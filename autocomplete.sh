if [[ $ZSH_NAME == "zsh" ]]; then
    autoload bashcompinit
    bashcompinit
fi

_my_autocomplete()
{
    local cur
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"

    subcommands_1="--delete --clear --list --full --recover"

    if [[ ${COMP_CWORD} == 1 ]] ; then
        COMPREPLY=( $(compgen -W "${subcommands_1}" -- ${cur}) )
        return 0
    fi

    subcmd_1="${COMP_WORDS[1]}"

    case "${subcmd_1}" in
    --delete )
        COMPREPLY=( $(compgen -W "`ls ${HOME}/.MyTrash`" -- ${cur}) )
        return 0 ;;

    --recover )
        COMPREPLY=( $(compgen -W "`ls ${HOME}/.MyTrash`" -- ${cur}) )
        return 0 ;;

    esac
    return 0
}

complete -F _my_autocomplete trash
