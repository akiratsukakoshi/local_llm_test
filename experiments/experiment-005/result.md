# Result

Status: model setup and human evaluation are in progress.

## Experimental caution

Both model generation and GPU changed. The GPU change from A5000 24GB to A40 48GB was required to fit the 23.25 GiB checkpoint plus runtime overhead. Capability and interactive speed must therefore be interpreted separately.

## Setup observation

The initial automatic AWQ backend selected Marlin and failed during `awq_marlin_repack`. This is a runtime/kernel compatibility failure, not evidence about model quality. The controlled retry explicitly selects Humming while retaining the same model and quantization.
