import  torch
import onnx


#net = torch.hub.load('milesial/Pytorch-UNet', 'unet_carvana', pretrained=True, scale=0.5)
net = torch.hub.load('mateuszbuda/brain-segmentation-pytorch', 'unet', in_channels=3, out_channels=1, init_features=32, pretrained=True)
net.eval()
dummy_input = torch.randn(1,3,224,224)
input_names = ['input']
output_names = ['output']

with torch.no_grad():
    xx = net(dummy_input)

torch.onnx.export(net, 
        dummy_input, 
        'unet.onnx', 
        verbose=True, 
        opset_version=11,
        input_names=input_names, 
        output_names=output_names, 
        export_params=True)
        #dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})
onnx_model = onnx.load('unet.onnx')
inferred_model = onnx.shape_inference.infer_shapes(onnx_model)
onnx.save(inferred_model, './unet/unet.onnx')
breakpoint()
