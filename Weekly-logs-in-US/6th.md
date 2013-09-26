#The 5th week in US
##Cloud Foudry
就在几周前，我们得知Cloud Foundry在这周末会举办一个展会，思科也会派人参加。得知消息后我们就跟Debo联系，看看有没有可能去参加一下。很快Debo就给我们搞到了免费的门票，但条件是我们要在思科的展位上展出点东西。

大家想了想，就剩一周不到的时间了，我们是做OpenStack的，那就把Cloud Foundry架到我们思科的OpenStack集群上试试。根据官网的[教程][1]，我们找来了BOSH，按照教程一步一步走，结果在部署micro bosh的时候出问题了，我们始终无法通过验证。即便手动ssh也进不去。其实，在思科的OpenStack上很多现成的image创建的VM都没法通过keypair登录进去，应该是VM创建后没有相应的更改ssh配置。

就在这个地方卡了我们好久，于是只好换用我们自己的server，但问题是，我们的server只有一个ip，没法创建floating ip。。。只好拜托鹏飞折腾一下，看看能不能搞个子网。另一方面，我们联系了思科内部OpenStack集群的负责人，虽然人家在休假，但还是出面帮我们排查问题。问题似乎出在，当我们用micro bosh把image上传到OpenStack创建VM后没有返回正确的metadata。。。

正当我们郁闷时，听说思科里已经有人把cloud foundry部署到VMware上了，我们跟他联系后得知可以用vagrant，最后，我们在展会现场把CF部署到OpenStack上。。。

##展会
第一次参加大型展会，刚签到就领到了衣服，进去以后发现各个公司的展位都在发衣服发礼品，转了一圈下来我们都收了有6、7件T恤了。会议开始后就是各公司的人轮番上台演讲，分享自己公司跟CF相关的业务，期间还有我们浙江大学的老师上台分享他们部署CF方面的心得。

参加展会除了有衣服的福利以外，当然还有美食，展会开了两天，我们蹭了两天饭。会议提供的是免费的自助餐，赞～此外，还碰到了一个带Google Glass的家伙，果断借来试了一把，虽然土鳖表示不太会用，实在是很高端的赶脚。

  [1]: http://docs.cloudfoundry.com/docs/running/deploying-cf/openstack/
