# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
# Author:      VollGaz
# -------------------------------------------------------------------------------






# Surcharge le parseur de base pour ajouter des commandes supplémentaires
def _create_arg_parser():
    description = 'crowd-controler'
    parser = utils.create_arg_parser(description, None)

    parser.add_argument('--group-memberships', metavar='GROUPNAME', type=str,
                        help='Display groups where the given group is nested (include inheritance)')
    parser.add_argument('--all-groups-memberships', action='store_true',
                        help='Display all the links between groups (include inheritance)')
    parser.add_argument('--show-all-groups', action='store_true', help='Display all groupes availables in crowd')
    parser.add_argument('--show-all-spaces', action='store_true', help='Display all spaces')
    parser.add_argument('--space-admin', metavar="SPACEKEY", type=str, help='Display space administrators')

    return parser


# Controleur principal de la ligne de commande
def commandline():
    parser = _create_arg_parser()
    args = utils.parse_args(parser)
    crowdtask = CrowdTasks(args)
    confluencetask = ConfluenceTasks()

    if args.group_memberships:
        raise NotImplementedError()

    elif args.all_groups_memberships:
        raise NotImplementedError()

    elif args.show_all_groups:
        raise NotImplementedError()

    elif args.space_admin:
        raise NotImplementedError()
