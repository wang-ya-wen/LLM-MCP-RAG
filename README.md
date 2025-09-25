创建python虚拟环境
conda create --name rag python=3.10
conda activate rag
#安装需要的依赖
pip install openai

由于代码中用到npx
在base环境中安装，安装步骤：
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 20
安装完后确认：
node -v
npm -v
npx -v
确认三个命令都有版本号输出。
npx -y @modelcontextprotocol/server-filesystem .
如果能启动，说明 fileMCP 就能用了。
