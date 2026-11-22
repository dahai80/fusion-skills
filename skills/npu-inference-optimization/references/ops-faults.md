# NPU Ops & Fault Handling (950DT container discipline)

## Wedged cards

- sync-fault debugging loops can wedge NPUs hard (campaign: davinci0/2,
  error 507035 → OS reboot required; subsequent processes fail first
  2 KB aclrtMalloc with 107002; npu-smi reset / docker restart ineffective,
  dms reports dev_info null).
- **Validate new shapes with single-shot runs. Never run fault loops on
  production cards.**

## Hop onto healthy cards

Same image + explicit `--device davinciN` passthrough → debug on healthy
cards with zero scheduling loss while wedged cards wait for the maintenance
window.

## dcmi "-8020 device in use" false positive

Idle containers still hold dcmi context and can masquerade as other errors
(e.g. triton get_arch SystemError from aclrtGetSocName NULL). Stop idle
containers on that card before creating a new one.

## Correct 950DT container device set

davinciN + davinci_manager + hisi_hdc + ummu + uburma. Missing
/dev/devmm_svm means a wrong device set — container creation fails.
Mount driver/dcmi/npu-smi/SFS following the production script.

## Process discipline

- md5 chain verification on every build (see custom-ops.md)
- losslessness judged by double-run noise baseline
- process data cleaned as produced; final artifacts archived (docs +
  SFS), e.g. campaign archive docs/e44_ascendc_project.md §8
