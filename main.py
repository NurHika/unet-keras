from model.unet import UNet
from tools.data import train_generator, test_generator, save_results

# TODO: move to config .json files
img_height = 512
img_width = 512
img_size = (img_height, img_width)
train_path = '/Users/vsevolod.konyahin/Desktop/DataSet/train'
test_path = '/Users/vsevolod.konyahin/Desktop/DataSet/test'
save_path = '/Users/vsevolod.konyahin/Desktop/DataSet/results'
model_name = 'unet_model.hdf5'
model_weights_name = 'unet_weight_model.hdf5'

if __name__ == "__main__":

    # generates training set
    train_gen = train_generator(
        batch_size = 2,
        train_path = train_path,
        image_folder = 'img',
        mask_folder = 'mask',
        target_size = img_size
    )


    # build model
    unet = UNet(
        input_size = (img_width,img_height,1),
        n_filters = 64,
        pretrained_weights = model_weights_name
    )
    unet.build()

    # createting a callback, hence best weights configurations will be saved
    model_checkpoint = unet.checkpoint(model_name)

    # model training
    # steps per epoch should be equal to number of samples in database divided by batch size
    # in this case, it is 528 / 2 = 264
    unet.fit_generator(
        train_gen,
        steps_per_epoch = 264,
        epochs = 5,
        callbacks = [model_checkpoint]
    )
    
    # saving model weights
    unet.save_model(model_weights_name)

    # generated testing set
    test_gen = test_generator(test_path, 30, img_size)

    # display results
    results = unet.predict_generator(test_gen,30,verbose=1)
    save_results(save_path, results)


