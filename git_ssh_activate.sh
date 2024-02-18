if [[ "$OSTYPE" == "msys" ]]; then
	eval `ssh-agent -s`
	ssh-add ~/.ssh/git_ed25519_key
else
	eval"$(ssh-agent -s)"
	ssh-add ~/.ssh/git_ed25519_key
fi