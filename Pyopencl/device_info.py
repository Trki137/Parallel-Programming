import pyopencl as cl

if __name__ == '__main__':
    platforms = cl.get_platforms()

    for platform in platforms:
        print(f"Platform: {platform.name}")
        print(f"Vendor: {platform.vendor}")
        print(f"Version: {platform.version}")
        print("Devices:")

        devices = platform.get_devices()
        for device in devices:
            print(f"  Device Name: {device.name}")
            print(f"  Device Type: {cl.device_type.to_string(device.type)}")
            print(f"  Device Memory: {device.global_mem_size / 1024 ** 2:.0f} MB")
            print(f"  Max Compute Units: {device.max_compute_units}")
            print(f"  Max Work Group Size: {device.max_work_group_size}")
            print()

        for device in devices:
            print(f"Device {device.name} Info:")
            print(f"  Max Clock Frequency: {device.max_clock_frequency} MHz")
            print(f"  Max Memory Allocation: {device.max_mem_alloc_size / 1024 ** 2:.0f} MB")
            print(f"  Local Memory: {device.local_mem_size / 1024:.0f} KB")
            print(f"  Image Support: {'Yes' if device.image_support else 'No'}")
            print(f"  OpenCL C Version: {device.opencl_c_version}")
            extensions = device.get_info(cl.device_info.EXTENSIONS)
            print("cl_khr_fp64" in extensions)
            print()
