# Current RunPod usage

After a Pod stop/restart, copy or use the scripts stored in `/workspace`:

```bash
/workspace/install_vllm.sh
tmux new-session -d -s vllm /workspace/serve_qwen25_coder_7b.sh
```

Check the API inside the Pod:

```bash
curl http://127.0.0.1:8000/v1/models
python3 /workspace/smoke_test.py
```

From WSL, create the private API tunnel using the current public IP and SSH port:

```bash
ssh -f -N \
  -o ExitOnForwardFailure=yes \
  -L 127.0.0.1:8000:127.0.0.1:8000 \
  -i ~/.ssh/id_ed25519 \
  -p SSH_PORT root@POD_IP
```

RunPod can change the public port after a stop/start, so retrieve the new `SSH over exposed TCP` command before recreating the tunnel.
