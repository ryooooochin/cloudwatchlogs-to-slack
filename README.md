# これは何

cloudwatch logsに特定の文字列が出たらslackに投稿するlambda  
SAMの設定して  
`code` フォルダ内で `pip install slackweb -t ./` してから  
`cd ../` → `make bucket` → `make all` でデプロイされるはず  
バケット名が他と被って作れない場合はMakefileを修正

# 使い方

1  
投稿先slackチャンネルのWebhook URLを取得  
https://qiita.com/vmmhypervisor/items/18c99624a84df8b31008  

2    
DynamoDBテーブル：cloudwatchlogs-to-slack-tableに以下値を登録  
id:任意(String)  
exclud:List（通知除外するStringを設定）  
loggroup:ロググループ名(String)  
webhookurl:↑で取得したWebhook URL(String)

3  
lambdaのトリガーを設定  
# 注意

ロググループに別のlambdaが設定されてたら使えない