/*	Polling Demo
*
*	Uses Polling Mode to acquire frames from the camera instead of using frame-available callbacks.
*	Reduces code complexity, but there is a chance to miss frames, especially if poll rate is slower
*	than frame rate.
*	This demo uses Software Triggering mode but also works with Hardware Triggering.
*/

/*	Color
*
*	Include tl_camera_sdk.h, tl_camera_sdk_load.h,tl_camera_sdk_load.c, thorlabs_tsi_color_error.h,
*	thorlabs_tsi_color_processing.h, thorlabs_tsi_demosaic.h, thorlabs_tsi_enum.h, thorlabs_tsi_LUT.h,
*	thorlabs_tsi_color_processing_load.h, thorlabs_tsi_color_processing_load.c, thorlabs_tsi_demosaic_load.h,
*	and thorlabs_tsi_demosaic_load.c in your project
*/


#include <stdio.h>
#include <stdlib.h>
#include "windows.h"
#include "tl_camera_sdk.h"
#include "tl_camera_sdk_load.h"
#include "thorlabs_tsi_color_error.h"
#include "thorlabs_tsi_enum.h"
#include "thorlabs_tsi_demosaic_load.h"
#include "thorlabs_tsi_color_processing_load.h"

// Close the SDK, then the dll
int close_sdk_dll(void) {
	int ret = 0;

	if (tl_camera_close_sdk())
	{
		printf("Failed to close SDK!\n");
		ret = 1;
	}

	if (tl_camera_sdk_dll_terminate())
	{
		printf("Failed to close dll!\n");
		ret = 1;
	}

	if (!ret) printf("SDK & dll closed\n");

	return ret;
}

int main(void)
{

	// Initializes dll
	if (tl_camera_sdk_dll_initialize())
	{
		printf("Failed to initialize dll!\n");
		return 1;
	}
	else printf("Successfully initialized dll\n");


	// Open the SDK
	if (tl_camera_open_sdk())
	{
		printf("Failed to open SDK!\n");
		tl_camera_sdk_dll_terminate();
		return 1;
	}
	else printf("Successfully opened SDK\n");

	char camera_ids[1024];

	void* camera_handle = 0;

	// Discover cameras.
	if (tl_camera_discover_available_cameras(camera_ids, 1024))
	{
		printf("Failed to get available cameras!\n");
		close_sdk_dll();
		return 1;
	}
	else printf("camera IDs: %s\n", camera_ids);

	// Check for no cameras.
	if (!strlen(camera_ids))
	{
		printf("Error: did not find any cameras!\n");
		close_sdk_dll();
		return 1;
	}

	// Camera IDs are separated by spaces.
	char* p_space = strchr(camera_ids, ' ');
	if (p_space)
	{
		*p_space = '\0'; // isolate the first detected camera
	}

	char first_camera[256];

	// Copy the ID of the first camera to separate buffer (for clarity)
	strcpy_s(first_camera, 256, camera_ids);

	printf("First camera_id = %s\n", first_camera);

	// Connect to the camera (get a handle to it).
	if (tl_camera_open_camera(first_camera, &camera_handle))
	{
		printf("Failed to open camera!\n");
		close_sdk_dll();
		return 1;
	}

	printf("Camera handle = 0x%Ix\n", (int)camera_handle);

	//initialize frame variables
	unsigned short *image_ptr = NULL;
	int frame_count = 0;
	int image_width = 0;
	int image_height = 0;
	int bit_depth = 0;
	int number_of_color_channels = 0;

	// Configure camera for continuous acquisition by setting the number of frames to 0.
	tl_camera_set_frames_per_trigger_zero_for_unlimited(camera_handle, 0);

	// Set camera to wait 10 ms for a frame to arrive during a poll.
	// If an image is not recieved in 10ms, the returned frame will be null
	int image_poll_timeout_ms = 10;
	int ret_val = 0;
	ret_val = tl_camera_set_image_poll_timeout(camera_handle, image_poll_timeout_ms);
	image_poll_timeout_ms = 0;
	ret_val = tl_camera_get_image_poll_timeout(camera_handle, &image_poll_timeout_ms);
	if (image_poll_timeout_ms != 10)
	{
		printf("timeout was not set!");
	}

	// Arm the camera
	if (tl_camera_arm(camera_handle, 2)) printf("Failed to arm the camera!\n");
	else printf("Camera armed\n");

	// Start the camera (done only once per acquisition run since we are continuously acquiring images).
	// For trigger modes (software or hardware), this would be called for every desired image.
	// Continuous acquisition is specified by setting the number of frames to 0 and issuing a single software trigger request.
	if (tl_camera_issue_software_trigger(camera_handle)) printf("Failed to start the camera!\n");
	else printf("Software trigger sent\n");

	//Poll for 1 image
	int count = 0;
	while (count < 1)
	{
		ret_val = tl_camera_get_pending_frame_or_null(camera_handle, &image_ptr, &image_width, &image_height, &bit_depth, &number_of_color_channels, &frame_count);
		if (ret_val != 0) // error codes are nonzero values
		{
			printf("Error while trying to get pending frame\n");
			continue;
		}
		if (!image_ptr)
		{
			continue;
		}
		printf("Pointer to Image: 0x%x\n", image_ptr);
		printf("Image width: %d, image height: %d\n", image_width, image_height);
		count++;
	}

	printf("Image received!\n");

	/**COLOR PROCESSING**/
	unsigned short *output_buf = (unsigned short *)malloc(sizeof(unsigned short) * image_width * image_height * 3); // color image size will be 3x the size of a mono image
	unsigned short *demosaic_buf = (unsigned short *)malloc(sizeof(unsigned short) * image_width * image_height * 3); // temporary buffer to store demosaic result
	//initialize demosaic module
	if (tl_demosaic_initialize())
	{
		printf("Failed to initialize demosaic module!");
	}
	// Demosaic the monochrome image data.
	// Create BGR Planer image data (BBBBBB... GGGGGG... RRRRRR...)
	if (tl_demosaic_transform_16_to_48(image_width, image_height, 0, 0, BAYER_BLUE, BGR_PLANAR, BAYER, 16, image_ptr, demosaic_buf))
	{
		printf("Failed to demosaic monochrome image!");
	}
	//initialize color processor module
	if (tl_color_processing_initialize())
	{
		printf("Failed to initialize color processing module!");
	}
	// Create a color processor instance.
	void* color_processor_inst = tl_color_create_color_processor(16, 16); // 16-bit image data
	if (!color_processor_inst)
	{
		printf("Failed to create a color processor instance!");
	}
	// configure sRGB output color space using matrices from camera
	float camera_color_correction_matrix[9];
	float camera_white_balance_matrix[9];
	if (tl_camera_get_color_correction_matrix(camera_handle, &camera_color_correction_matrix))
	{
		printf("Failed to get color correction matrix from camera!");
	}
	if (tl_camera_get_default_white_balance_matrix(camera_handle, &camera_white_balance_matrix))
	{
		printf("Failed to get white balance matrix from camera!");
	}
	if (tl_color_append_matrix(color_processor_inst, camera_color_correction_matrix))
	{
		printf("Failed to append color correction matrix!");
	}
	if (tl_color_append_matrix(color_processor_inst, camera_white_balance_matrix))
	{
		printf("Failed to append white balance matrix!");
	}
	// Use the output LUTs to configure the sRGB nonlinear (companding) function.
	sRGB_companding_LUT(16, tl_color_get_blue_output_LUT(color_processor_inst));
	sRGB_companding_LUT(16, tl_color_get_green_output_LUT(color_processor_inst));
	sRGB_companding_LUT(16, tl_color_get_red_output_LUT(color_processor_inst));
	int err_code = tl_color_transform_48_to_48(color_processor_inst
		, demosaic_buf        // input buffer
		, BGR_PLANAR          // input buffer format
		, 0                   // blue minimum clamp value
		, ((1 << 16) - 1)     // blue maximum clamp value (14 bit pixel data)
		, 0                   // green minimum clamp value
		, ((1 << 16) - 1)     // green maximum clamp value
		, 0                   // red minimum clamp value
		, ((1 << 16) - 1)     // red maximum clamp value
		, 0                   // blue shift distance
		, 0                   // green shift distance
		, 0                   // red shift distance
		, output_buf          // output buffer
		, BGR_PIXEL           // output buffer format
		, image_width * image_height);
	if (err_code)
	{
		printf("Failed to color process the demosaic color frame!\n");
	}
	// Destroy the color processor instance.
	if (tl_color_destroy_color_processor(color_processor_inst) != TL_COLOR_NO_ERROR)
	{
		printf("Failed to destroy the color processor instance!\n");
	}
	// Clean up.
	free(demosaic_buf);
	// Terminate the color processing module
	if (tl_color_processing_terminate() != TL_COLOR_NO_ERROR)
	{
		printf("Failed to terminate the color processing module!\n");
	}
	// Terminate the demosaic module.
	if (tl_demosaic_terminate() != TL_COLOR_NO_ERROR)
	{
		printf("Failed to terminate the demosaic library!\n");
	}
	//Do stuff with color image
	printf("Done with image!\n");
	free(output_buf);

	// Stop the camera.
	if (tl_camera_disarm(camera_handle))
	{
		printf("Failed to stop the camera!\n");
	}

	// Close the camera.
	if (tl_camera_close_camera(camera_handle))
	{
		printf("Failed to close camera!\n");
	}
	camera_handle = 0;

	// Free the C Camera SDK followed by the Unified SDK
	if (close_sdk_dll()) return 1;
	else return 0;

}

