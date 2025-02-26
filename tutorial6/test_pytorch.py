import pytest, torch

@pytest.fixture
def x_gpu():
    return torch.Tensor([42]).cuda()

@pytest.mark.gpu
def test_cuda(x_gpu):
	assert x_gpu.is_cuda
	assert not x_gpu.cpu().is_cuda
