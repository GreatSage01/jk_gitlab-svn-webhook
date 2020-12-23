##### 获取自签名公钥
```shell
openssl s_client -showcerts -connect 192.168.66.186:8443
```
> svnSelfSignedRootCA.crt
```shell
-----BEGIN CERTIFICATE-----
MIIC9zCCAd+gAwIBAgIJAJbCWK0vZD0sMA0GCSqGSIb3DQEBCwUAMBoxGDAWBgNV
BAMMD1dJTi1KRkxMOVJUSjc2TTAeFw0xODA3MjkwOTU4NTVaFw0yODA3MjYwOTU4
NTVaMBoxGDAWBgNVBAMMD1dJTi1KRkxMOVJUSjc2TTCCASIwDQYJKoZIhvcNAQEB
BQADggEPADCCAQoCggEBANQU3EDbdkn7yVFh6ozRbPFp5sbE6be2RjYHfTtI5J0m
uTHlrZabVNjpcmNM4BK07QsS5b8vdpLcGDO1RzUi0Zh2fcspzEF35J2E3uJRqyGO
HUM2CVMqgBkh3FqhHVHcbdcReYDisu+GDGQIUACzzavtxooFDHPQv2VoPSeqhmWv
gq7UkS6NIyraJ7rSytleUvkwCcAVF06WDBXFjF0esQSmq0JxGpo9gnBC/THD/tIb
Iwazp4PgQhesc3qqusLxhh064KpL8g2rPlE/OfbEotae1/yIS6aeGf6qiJ7MEC83
z7eqiNwUXt+8BbEFsOiCLaciIs2DeFTc3j/Mzv2eRi0CAwEAAaNAMD4wCwYDVR0P
BAQDAgQwMBMGA1UdJQQMMAoGCCsGAQUFBwMBMBoGA1UdEQQTMBGCD1dJTi1KRkxM
OVJUSjc2TTANBgkqhkiG9w0BAQsFAAOCAQEAFg8DrrW9ZscxxQ+gq4fxGcL7A3OX
LrQTPu4hdhUieEkuB/z+K5lqSJuya5MWjW3gDX8pbxOqcIg9Wc9n0R/WPWQvJR+L
Y0Q3x+EfapghRnXHVlV1kBLObh1034zWSk6P8+1WqClB6vHzvOb0rp6Hlt4uPPHY
fV7cz6fVMRAGoQBNnYM11EXVXPoTAJNWZV9YLiT48pkrPL8zYseImpSQZMmq9Pvw
xvtKi57ddLG+RLjQvPrUQo7QezKcWFhCh2n22BZ1BtNpqyeeN9EB1c9uKCUsbrgB
PfDAYImqOVtaVFpxUTMMMgBgJVKotAd9o9FerfJzPMvMmSKFBktznJd5EQ==
-----END CERTIFICATE-----
```


##### 启动容器
```shell
docker run -d \
    -p 8888:8888 \
    --name=jk_gitlab-svn-webhook \
    --restart=always \
    hub.xueerqin.net/base/jk_gitlab-svn-webhook:0.0.7
```