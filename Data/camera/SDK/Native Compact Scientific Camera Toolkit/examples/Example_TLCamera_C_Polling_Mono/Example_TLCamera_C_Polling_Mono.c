/*	Polling
*
*	Uses Polling Mode to acquire frames from the camera instead of using frame-available callbacks.
*	Reduces code complexity, but there is a chance to miss frames, especially if poll rate is slower
*	than frame rate.
*	This demo uses Software Triggering mode but also works with Hardware Triggering.
*/

/*	Monochrome
*
*	Include tl_camera_sdk.h, thorlabs_tsi_enum.h, tl_camera_sdk_load.h, and tl_camera_sdk_load.c in your project
*/


#include <stdio.h>
#include <stdlib.h>
#include "tl_camera_sdk.h"
#include "tl_camera_sdk_load.h"

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

	//Poll for 10 images
	int count = 0;
	while (count < 10)
	{
		ret_val = tl_camera_get_pending_frame_or_null(camera_handle, &image_ptr, &image_width, &image_height, &bit_depth, &number_of_color_channels, &frame_count);
		if (ret_val != 0) // error codes are nonzero values
		{
			printf("Error while trying to get pending frame!\n");
			break;
		}
		if (!image_ptr)
		{
			continue; //timeout
		}
		printf("Pointer to Image: 0x%x\n", image_ptr);
		printf("Image width: %d, image height: %d\n", image_width, image_height);
		count++;
	}

	printf("Images received! Closing camera...\n");

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

