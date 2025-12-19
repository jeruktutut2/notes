# SWIFT

## install
    # Install swiftenv
    brew install kylef/formulae/swiftenv
    echo 'eval "$(swiftenv init -)"' >> ~/.zshrc
    exec zsh

    # Install Swift versi backend (misal versi 6.0)
    swiftenv install 6.0
    swiftenv global 6.0  # atau local di folder project

    # Buat project backend
    mkdir MyBackend && cd MyBackend
    swift package init --type executable

    # (opsional) Tambahkan framework backend seperti Vapor
    swift package add https://github.com/vapor/vapor.git
    swift build
    swift run

    curl -O https://download.swift.org/swiftly/darwin/swiftly.pkg && \
installer -pkg swiftly.pkg -target CurrentUserHomeDirectory && \
~/.swiftly/bin/swiftly init --quiet-shell-followup && \
. "${SWIFTLY_HOME_DIR:-$HOME/.swiftly}/env.sh" && \
hash -r

swiftenv local 6.0
    swift --version