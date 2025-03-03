#!/bin/bash

sudo apt-get install zsh -y
sudo curl -L http://install.ohmyz.sh | sh
chsh -s $(which zsh)

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
#*------------------------------------------------------------------------------
# First, remove the problematic OpenSUSE repository
sudo rm /etc/apt/sources.list.d/zsh-autosuggestions.list
sudo rm /etc/apt/trusted.gpg.d/zsh-autosuggestions.gpg

# Make sure universe repository is enabled
sudo add-apt-repository universe

# Update and install
sudo apt update
sudo apt install zsh-autosuggestions

source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh
source ~/.zshrc
#*------------------------------------------------------------------------------
# Backup existing .zshrc
cp ~/.zshrc ~/.zshrc.backup

# Add zsh-autosuggestions configuration
echo '
# Enable zsh-autosuggestions
source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# Autosuggestions configuration
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=8"
ZSH_AUTOSUGGEST_STRATEGY=(history completion)
ZSH_AUTOSUGGEST_BUFFER_MAX_SIZE=20
' >> ~/.zshrc

# Reload zsh configuration
source ~/.zshrc
#*------------------------------------------------------------------------------
conda init zsh