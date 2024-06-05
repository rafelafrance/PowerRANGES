#!/bin/bash

SESSION="power"
TRAIT="$HOME/work/traiter"
MISC="$HOME/work/misc"

tmux new -s $SESSION -d
tmux rename-window -t $SESSION ranges
tmux send-keys -t $SESSION "cd $TRAIT/PowerRANGES" C-m
tmux send-keys -t $SESSION "vrun .venv" C-m
tmux send-keys -t $SESSION "git status" C-m

tmux new-window -t $SESSION
tmux send-keys -t $SESSION "cd $TRAIT/PowerRANGES" C-m
tmux send-keys -t $SESSION "vrun .venv" C-m

tmux select-window -t $SESSION:1
tmux attach -t $SESSION
