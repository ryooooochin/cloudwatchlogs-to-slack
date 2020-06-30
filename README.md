# これは何

cloudwatch logsに特定の文字列が出たらslackに投稿するlambda  
SAMの設定してデプロイ用のバケット（Makefileに記載）を用意すれば  
`code` フォルダ内で `pip install slackweb -t ./` してから  
`cd ../` → `make all` でデプロイされるはず

# 使い方

投稿先slackチャンネルのWebhook URLを取得  
https://qiita.com/vmmhypervisor/items/18c99624a84df8b31008  
  
ロググループ名、Webhookurl、除外文字列をDynamoDBに登録  
テーブル名：cloudwatchlogs-to-slack-table  
  
lambdaのトリガーを設定  
関数名：cloudwatchlogs-to-slack-function  

# 注意

ロググループに別のlambdaが設定されてたら使えない