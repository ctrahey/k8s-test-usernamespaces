# Testing UserNamespaces in Kubernetes on EC2

This project is a test setup for evaulating the new user namespaces feature in Kubernetes.
Because the feature is currently behind an alpha feature-flag, we setup a Kubernetes control
plane manually in EC2, using the "stock" EKS AMI (currently for 1.25) but adding a build of
containerd from the 1.7 release candidate.

This is the command I use to deploy the stack:
```bash
KEYPAIR_NAME=some_keypair_name
aws cloudformation create-stack --stack-name testns --template-body file://stack.cf.yaml --parameters ParameterKey=KeyPair,ParameterValue=$KEYPAIR_NAME --capabilities CAPABILITY_NAMED_IAM --disable-rollback
```

When this ends, there will be two EC2 instances. The first will have bootstrapped a cluster, and you will find the results of that in /var/log/cloud-init-output.log
From there, you can copy the worker-node join command (or generate a new one) and run it on the second instance. You can also grab the kubeconfig from the first node 
(so you don't have to mint a new user/CSR etc. for this simple test case). Once the worker is up and you have a kubectl configured to talk to the cluster, submit the
test workloads, then login to the worker node and start evaluating... did the `hostUsers: false` pod get a user namespace provisioned?

Current results: No - need to dig further.

@todo: Automate more tasks:
1. Joining worker node to cluster
1. deploying the test workload
1. simplify reading of results (confirming if user namespace is being used)


Notes for confirming
```bash
pstree -N user
journalctl --since "2013-03-13 18:42:11" --until "2013-03-13 18:42:22"
```