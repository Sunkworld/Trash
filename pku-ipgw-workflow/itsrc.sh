touch ~/.its
query='{query}'
echo {query} > ~/.its
arr=($query)
echo 网关配置成功
echo 账号: ${arr[0]}, 密码: ${arr[1]}
