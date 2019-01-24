#include <stdio.h>
#include <errno.h>
#include <iio.h>


struct iio_device_info {
	struct iio_device *device;
	unsigned int id;
	const char* name;
	unsigned int channel_count;
	struct iio_channel **channels;
	unsigned int attr_count;
	const char** attrs;
	unsigned int buffer_attr_count;
	const char** buffer_attrs;
};


// Wrapper function to create default IIO_Context.
// Exist program if unable to create a context.
// Printing the error code.
struct iio_context *create_context() {
	// Create IIO_Context
	struct iio_context *context = iio_create_default_context();

	// Unable to create a context due to no available contexts
	if(context == NULL) {
		printf("Could not create a local context\n");
		int errsv = errno;
		printf("Error: Context Error Code: %d\n", errsv);
		exit(1);
	}
	return context;
}

struct iio_channel **get_iio_channels(struct iio_device *dev, unsigned int num_channels) {
	struct iio_channel **channels = malloc(sizeof(struct iio_channel*) * num_channels);
	unsigned int i;
	for(i = 0; i < num_channels; i++) {
		channels[i] = iio_device_get_channel(dev, i);
	}
	return channels;
}


const char **get_attrs(struct iio_device *dev, unsigned int num_attrs) {
	const char** attrs = malloc(sizeof(char *) * num_attrs);
	unsigned int i;
	for(i = 0; i < num_attrs; i++) {
		attrs[i] = iio_device_get_attr(dev, i);
	}
	return attrs;
}

const char **get_buffer_attrs(struct iio_device *dev, unsigned int num_buf_attrs) {
	const char** buffer_attrs = malloc(sizeof(char *) * num_buf_attrs);
	unsigned int i;
	for(i = 0; i < num_buf_attrs; i++) {
		buffer_attrs[i] = iio_device_get_buffer_attr(dev, i);
	}
	return buffer_attrs;
}

// Obtains an array of pointers to iio_devices
struct iio_device_info **get_iio_devices(struct iio_context *ctx) {
	unsigned int num_devices = 
		iio_context_get_devices_count(ctx);

	struct iio_device_info **devices = 
		malloc(sizeof(struct iio_device_info*) * num_devices);

	unsigned int i;
	for(i = 0; i < num_devices; i++) {

		struct iio_device *device = iio_context_get_device(ctx, i);
		if(device == NULL) {
			printf("Could not get device %d\n", i);
			exit(1);
		}

		devices[i] = malloc(sizeof(struct iio_device_info));
		devices[i]->device = device;
		devices[i]->name = iio_device_get_name(device);
		devices[i]->id = i;
		devices[i]->channel_count = 
			iio_device_get_channels_count(device);
		devices[i]->attr_count =
			iio_device_get_attrs_count(device);
		devices[i]->buffer_attr_count = 
			iio_device_get_buffer_attrs_count(device);
		devices[i]->channels = get_iio_channels(device, devices[i]->channel_count);
		devices[i]->attrs = get_attrs(device, devices[i]->attr_count);
		devices[i]->buffer_attrs = get_buffer_attrs(device, devices[i]->buffer_attr_count);
	}
	return devices;
}



int main() {
	
	struct iio_context *context = create_context();
	const char *ctx_name = iio_context_get_name(context);
		printf("Context Name: %s\n", ctx_name);	
	// iio_devices is an array of pointers pointing to each iio_device
	struct iio_device_info **iio_devices = get_iio_devices(context);

	

	//Destroy IIO_Context
	iio_context_destroy(context);
	return 0;
}
