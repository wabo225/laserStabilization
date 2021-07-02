#include "./SDK/Native Compact Scientific Camera Toolkit/include/tl_camera_sdk.h"
#include "./SDK/Native Compact Scientific Camera Toolkit/include/tl_camera_sdk_load.h"
#include "stdio.h"

int main() {
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
    
    char cameraIds[1024];
    void* camera_handle = 0;
    printf(tl_camera_discover_available_cameras(cameraIds, 1024));
    return 0;
}