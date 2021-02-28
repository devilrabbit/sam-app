import * as AWS from "aws-sdk";

export const localConfigure = () => {
  AWS.config.update(
    {
      region: "ap-northeast-1",
      endpoint: process.env.AWS_LOCAL_URL,
      AccessKeyId: "fakeAccessKeyId",
      SecretAccessKey: "fakeSecretAccessKey"
    },
    true
  );
}