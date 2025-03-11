FROM mcr.microsoft.com/devcontainers/cpp:debian

ENV TOOLCHAIN_VERSION=14.2.rel1
ENV TOOLCHAIN_ARCH=aarch64
# aarch64 or x86_64

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    clang-format \
    pipx \
    python3-pil \
    python3-pip

RUN curl -s -L https://developer.arm.com/-/media/Files/downloads/gnu/${TOOLCHAIN_VERSION}/binrel/arm-gnu-toolchain-${TOOLCHAIN_VERSION}-${TOOLCHAIN_ARCH}-arm-none-eabi.tar.xz | tar xJf - -C /opt

RUN P=$(ls -d /opt/arm-gnu-toolchain-*/bin | head -1) && \
    echo "export PATH=\$PATH:$P" >> /etc/profile

RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin/

USER vscode
RUN pipx install black


