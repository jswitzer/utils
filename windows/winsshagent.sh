# Modified from https://help.github.com/articles/working-with-ssh-key-passphrases/#platform-windows
# Also from http://stackoverflow.com/questions/3669001/getting-ssh-agent-to-work-with-git-run-from-windows-command-shell/15870387#15870387
# The main difference is just exporting an environment.bat that can be sourced
export SSH_ENV="$HOME/.ssh/environment"

function start_agent {
    echo "Initializing new SSH agent..."
    # spawn ssh-agent
    ssh-agent | sed 's/^echo/#echo/' > "$SSH_ENV"
    echo succeeded
    chmod 600 "$SSH_ENV"
    . "$SSH_ENV" > /dev/null
    echo "SET SSH_AUTH_SOCK=$SSH_AUTH_SOCK" > "$SSH_ENV.bat"
    echo "SET SSH_AGENT_PID=$SSH_AGENT_PID" >> "$SSH_ENV.bat"
    echo "Adding Default identity"
    ssh-add
}

# test for identities
function test_identities {
    # test whether standard identities have been added to the agent already
    ssh-add -l | grep "The agent has no identities" > /dev/null
    if [ $? -eq 0 ]; then
        ssh-add
        # $SSH_AUTH_SOCK broken so we start a new proper agent
        if [ $? -eq 2 ];then
            start_agent
        else
            if [ -e $HOME/.ssh/agent_keys]; then
              for x in $HOME/.ssh/agent_keys/* ; do 
                echo "Adding $x"
                ssh-add $x
              done
            fi
        fi
    fi
}

# check for running ssh-agent with proper $SSH_AGENT_PID
if [ -n "$SSH_AGENT_PID" ]; then
    ps -f -u $USERNAME | grep "$SSH_AGENT_PID" | grep ssh-agent > /dev/null
    if [ $? -eq 0 ]; then
        test_identities
    else
        start_agent
    fi
else
    if [ -f "$SSH_ENV" ]; then
    . "$SSH_ENV" > /dev/null
    fi
    ps -f -u $USERNAME | grep "$SSH_AGENT_PID" | grep ssh-agent > /dev/null
    if [ $? -eq 0 ]; then
        test_identities
    else
        start_agent
    fi
fi
