complete --command timetracking --exclusive --short-option p --long-option project --arguments "(timetracking list)" --description "select project"
complete --command timetracking --no-files --short-option c --long-option continue --description "also continue tracking other projects"
complete --command timetracking --no-files --arguments "start end list"
complete --command timetracking --no-files --arguments add --description "add project to project list"
complete --command timetracking --no-files --short-option a --long-option active --description "only active projects"

complete --command timetracking --no-files --short-option h --long-option help --description "show help"
