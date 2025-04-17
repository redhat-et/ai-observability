#!/usr/bin/env python3

import os
import json
import uuid
import time
import platform
import psutil

try:
    import torch
    has_torch = True
except ImportError:
    has_torch = False

CONFIG_PATH = "/home/vllm/.config/vllm"
os.makedirs(CONFIG_PATH, exist_ok=True)
output_file = os.path.join(CONFIG_PATH, "usage_stats.json")

data = {}

data["uuid"] = str(uuid.uuid4())

data["log_time"] = int(time.time() * 1e9)

data["architecture"] = platform.machine()
data["platform"] = platform.platform()
data["cpu_type"] = platform.processor()
data["cpu_family_model_stepping"] = ", ".join(map(str, platform.uname()))
data["num_cpu"] = psutil.cpu_count()
data["total_memory"] = psutil.virtual_memory().total

if has_torch and torch.cuda.is_available():
    data["gpu_count"] = torch.cuda.device_count()
    data["gpu_type"] = torch.cuda.get_device_name(0)
    data["gpu_memory_per_device"] = torch.cuda.get_device_properties(0).total_memory
else:
    data["gpu_count"] = 0
    data["gpu_type"] = None
    data["gpu_memory_per_device"] = 0

data["provider"] = os.environ.get("PROVIDER", "unknown")
data["source"] = os.environ.get("VLLM_SOURCE", "production")
data["context"] = os.environ.get("VLLM_CONTEXT", "LLM_CLASS")
data["vllm_version"] = os.environ.get("VLLM_VERSION", "0.7.3")  # adjust if pinned
data["model_architecture"] = os.environ.get("MODEL_ARCH", "unknown")
data["dtype"] = os.environ.get("DTYPE", "torch.float16")

data["tensor_parallel_size"] = int(os.environ.get("TP_SIZE", 1))
data["block_size"] = int(os.environ.get("BLOCK_SIZE", 16))
data["gpu_memory_utilization"] = float(os.environ.get("GPU_UTIL", 0.0))
data["quantization"] = os.environ.get("QUANTIZATION", None)
data["kv_cache_dtype"] = os.environ.get("KV_CACHE_DTYPE", "auto")
data["enable_lora"] = os.environ.get("ENABLE_LORA", "false") == "true"
data["enable_prefix_caching"] = os.environ.get("ENABLE_PREFIX_CACHE", "false") == "true"
data["enforce_eager"] = os.environ.get("ENFORCE_EAGER", "false") == "true"
data["disable_custom_all_reduce"] = os.environ.get("DISABLE_CUSTOM_ALL_REDUCE", "true") == "true"

with open(output_file, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ usage_stats.json written to: {output_file}")
