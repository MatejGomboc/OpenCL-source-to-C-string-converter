#define M_2_PI 6.283185307179586476925286766559f
#define M_PI_2 1.5707963267948966192313216916398f
#define M_PI 3.1415926535897932384626433832795f

kernel void mandelbrot (
		write_only image2d_t output_image,
		const float x_min,
		const float x_max,
		const float y_min,
		const float y_max,
		const uint max_iterations
	)
{
	float x0 = ((float)get_global_id(0) / (float)get_global_size(0)) * (x_max - x_min) + x_min;
	float y0 = ((float)get_global_id(1) / (float)get_global_size(1)) * (y_max - y_min) + y_min;

	float x = 0.0f;
	float y = 0.0f;
	uint iteration = 0;
	float temp = 0.0f;

	while ((x*x + y*y < 2.0f * 2.0f) && (iteration < max_iterations))
	{
		temp = x*x - y*y + x0;
		y = 2.0f * x*y + y0;
		x = temp;
		iteration = iteration + 1;
	}
	
	float quotient = (float)iteration / (float)max_iterations;

	write_imagef(output_image, (int2)(get_global_id(0), get_global_id(1)), (float4)(
		0.5f * sin(M_2_PI * quotient - M_PI) + 0.5f,
		0.5f * sin(M_2_PI * quotient - M_PI_2) + 0.5f,
		0.5f * sin(M_2_PI * quotient) + 0.5f,
		1.0f
	));
}
