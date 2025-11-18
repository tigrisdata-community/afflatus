#!/usr/bin/env bash

uv python install &
uv sync &
npm ci &
npm install -g @anthropic-ai/claude-code &

wait
