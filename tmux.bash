#!/bin/bash

SESSION="power"
TRAIT="$HOME/work/traiter"

tmux new -s $SESSION -d
tmux rename-window -t $SESSION ranges
tmux send-keys -t $SESSION "cd $TRAIT/PowerRANGES" C-m
tmux send-keys -t $SESSION "vrun .venv" C-m
tmux send-keys -t $SESSION "git status" C-m

tmux new-window -t $SESSION
tmux rename-window -t $SESSION traiter
tmux send-keys -t $SESSION "cd $TRAIT/traiter" C-m
tmux send-keys -t $SESSION "vrun .venv" C-m
tmux send-keys -t $SESSION "git status" C-m

tmux new-window -t $SESSION
tmux rename-window -t $SESSION vertnet
tmux send-keys -t $SESSION "cd $TRAIT/vertnet" C-m
tmux send-keys -t $SESSION "vrun .venv" C-m
tmux send-keys -t $SESSION "git status" C-m

tmux new-window -t $SESSION
tmux rename-window -t $SESSION util
tmux send-keys -t $SESSION "cd $MISC/common_utils" C-m
tmux send-keys -t $SESSION "vrun .venv" C-m
tmux send-keys -t $SESSION "git status" C-m

tmux new-window -t $SESSION

tmux select-window -t $SESSION:1
tmux attach -t $SESSION
