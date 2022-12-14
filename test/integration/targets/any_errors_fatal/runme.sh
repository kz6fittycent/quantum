#!/usr/bin/env bash

set -ux
quantum-coupling -i inventory "$@" play_level.yml| tee out.txt | grep 'any_errors_fatal_play_level_post_fail'
res=$?
cat out.txt
if [ "${res}" -eq 0 ] ; then
	exit 1
fi

quantum-coupling -i inventory "$@" on_includes.yml | tee out.txt | grep 'any_errors_fatal_this_should_never_be_reached'
res=$?
cat out.txt
if [ "${res}" -eq 0 ] ; then
	exit 1
fi

set -ux

quantum-coupling -i inventory "$@" always_block.yml | tee out.txt | grep 'any_errors_fatal_always_block_start'
res=$?
cat out.txt
exit $res
