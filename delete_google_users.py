#!/usr/bin/env python3
"""
Delete named users from Google Workspace, reusing the GWAPS daemon's own
credentials and service builder.

Dry run by default, matching the daemon's convention. Nothing is deleted
without --apply.

Deleting the Google user also removes every group membership it held, so
the wrongly named class group needs no separate cleanup.

Safe to run while gwaps.service is up: these users' GOOGLE provisioning rows
are PROVISIONED, and the daemon's claim query only takes PENDING, due FAILED
or stale PROCESSING rows, so it will not recreate them.

Usage
    sudo python3 delete_google_users.py                     # dry run
    sudo python3 delete_google_users.py --apply             # delete
    sudo python3 delete_google_users.py --apply a@x b@y     # override the list
"""
import argparse
import os
import sys

GWAPS_DIR = '/home/ubuntu/EduNeX/edunex-provisioning-service/gwaps'
ENV_FILE = '/etc/gwaps/gwaps.env'

DEFAULT_ACCOUNTS = [
    "698109901@stu.edunex.edu.pg",
    "698109902@stu.edunex.edu.pg",
    "698109903@stu.edunex.edu.pg",
    "698109904@stu.edunex.edu.pg",
]


def load_env(path):
    """Pick up GOOGLE_APPLICATION_CREDENTIALS and friends the unit file sets."""
    if not os.path.exists(path):
        print("note: %s not found, relying on the ambient environment" % path)
        return
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                os.environ.setdefault(k, v)
    except PermissionError:
        print("error: cannot read %s, run this with sudo" % path)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true',
                    help='actually delete; omit for a dry run')
    ap.add_argument('accounts', nargs='*', default=None,
                    help='email addresses; defaults to the four test accounts')
    args = ap.parse_args()

    accounts = args.accounts or DEFAULT_ACCOUNTS

    load_env(ENV_FILE)
    sys.path.insert(0, GWAPS_DIR)
    import gwaps_daemon as g

    svc = g.get_service()
    print("mode: %s\n" % ("APPLY, deletions are real" if args.apply else "dry run"))

    missing = 0
    deleted = 0
    for email in accounts:
        u = g.get_user(svc, email)
        if not u:
            print("%-32s not in google workspace" % email)
            missing += 1
            continue

        ou = u.get('orgUnitPath', '?')
        try:
            groups = g.current_groups(svc, email)
        except Exception as ex:
            groups = ['<could not list: %s>' % ex]

        print("%-32s ou=%s" % (email, ou))
        for grp in sorted(groups):
            print("%-32s   group %s" % ("", grp))

        if not args.apply:
            print("%-32s   would delete\n" % "")
            continue

        try:
            svc.users().delete(userKey=email).execute()
            print("%-32s   DELETED\n" % "")
            deleted += 1
        except Exception as ex:
            print("%-32s   FAILED: %s\n" % ("", ex))

    print("---")
    print("%d account(s) considered, %d not present, %d deleted"
          % (len(accounts), missing, deleted))
    if not args.apply:
        print("dry run, nothing changed. Re-run with --apply to delete.")
    else:
        print("Next: Keycloak, then the database rows.")


if __name__ == '__main__':
    main()
