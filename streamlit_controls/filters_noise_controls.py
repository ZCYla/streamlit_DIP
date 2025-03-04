# streamlit_controls/filters_noise_controls.py

import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
from image_processing.basic_operations import convert_to_grayscale
from image_processing.filters_and_noise import (
    add_noise, mean_filter, median_filter, gaussian_filter, bilateral_filter, sharpen_filter,
    apply_frequency_filter_to_image, homomorphic_filter)

def filters_noise_control(image_controller):
    """控制滤波和噪声添加的界面，如均值滤波、添加高斯噪声等。"""
    st.sidebar.subheader("滤波与噪声")

    current_image = image_controller.get_current_image()
    if st.sidebar.checkbox("添加噪声"):
        current_image = image_controller.get_current_image()
        if current_image is None:
            st.sidebar.info("请先上传一张图像以使用滤波与噪声操作。")
            return
        noise_type = st.sidebar.selectbox("选择噪声类型", ["高斯噪声", "盐和胡椒噪声", "泊松噪声", "斑点噪声"])

        if noise_type == "高斯噪声":
            mean = st.sidebar.slider("均值", -50.0, 50.0, 0.0, 0.1)
            sigma = st.sidebar.slider("标准差", 0.0, 100.0, 25.0, 1.0)
            if st.sidebar.button("应用高斯噪声"):
                image_controller.apply_operation(add_noise, noise_type="gaussian", mean=mean, sigma=sigma)
                st.success("高斯噪声已添加。")

        elif noise_type == "盐和胡椒噪声":
            amount = st.sidebar.slider("噪声比例", 0.0, 1.0, 0.02, 0.01)
            s_vs_p = st.sidebar.slider("盐与胡椒比例", 0.0, 1.0, 0.5, 0.1)
            if st.sidebar.button("应用盐和胡椒噪声"):
                image_controller.apply_operation(add_noise, noise_type="salt and pepper", amount=amount, s_vs_p=s_vs_p)
                st.success("盐和胡椒噪声已添加。")

        elif noise_type == "泊松噪声":
            scale = st.sidebar.slider("泊松噪声缩放因子", 1.0, 10.0, 1.0, 0.1)
            if st.sidebar.button("应用泊松噪声"):
                image_controller.apply_operation(add_noise, noise_type="poisson")
                st.success("泊松噪声已添加。")

        elif noise_type == "斑点噪声":
            speckle_scale = st.sidebar.slider("斑点噪声比例", 0.0, 1.0, 0.5, 0.1)
            if st.sidebar.button("应用斑点噪声"):
                image_controller.apply_operation(add_noise, noise_type="speckle", speckle_scale=speckle_scale)
                st.success("斑点噪声已添加。")

    if st.sidebar.checkbox("空域滤波"):
        if current_image is None:
            st.sidebar.info("请先上传一张图像以使用滤波与噪声操作。")
            return
        filter_type = st.sidebar.selectbox("选择滤波器", ["均值滤波", "中值滤波", "高斯滤波", "双边滤波"])
        if filter_type == "均值滤波":
            kernel_size = st.sidebar.slider("滤波器大小", 1, 51, 3, 2)
            if st.sidebar.button("应用均值滤波"):
                image_controller.apply_operation(mean_filter, kernel_size=kernel_size)
                st.success(f"均值滤波已应用，核大小={kernel_size}。")
                # st.image(image_controller.get_current_image(), caption=f"均值滤波器大小: {kernel_size}", use_container_width=True)

        elif filter_type == "中值滤波":
            kernel_size = st.sidebar.slider("滤波器大小", 1, 51, 3, 2)
            if st.sidebar.button("应用中值滤波"):
                image_controller.apply_operation(median_filter, kernel_size=kernel_size)
                st.success(f"中值滤波已应用，核大小={kernel_size}。")
                # st.image(image_controller.get_current_image(), caption=f"中值滤波器大小: {kernel_size}", use_container_width=True)

        elif filter_type == "高斯滤波":
            kernel_size = st.sidebar.slider("滤波器大小", 1, 51, 3, 2)
            sigma = st.sidebar.slider("标准差", 0.0, 100.0, 0.0, 1.0)
            if st.sidebar.button("应用高斯滤波"):
                image_controller.apply_operation(gaussian_filter, kernel_size=kernel_size, sigma=sigma)
                st.success(f"高斯滤波已应用，核大小={kernel_size}, sigma={sigma}。")
                # st.image(image_controller.get_current_image(), caption=f"高斯滤波器大小: {kernel_size}, sigma: {sigma}", use_container_width=True)

        elif filter_type == "双边滤波":
            diameter = st.sidebar.slider("直径 (diameter)", 1, 25, 9)
            sigma_color = st.sidebar.slider("颜色空间的标准差 (sigma_color)", 1, 150, 75)
            sigma_space = st.sidebar.slider("坐标空间的标准差 (sigma_space)", 1, 150, 75)
            if st.sidebar.button("应用双边滤波"):
                image_controller.apply_operation(bilateral_filter, diameter=diameter, sigma_color=sigma_color, sigma_space=sigma_space)
                st.success(f"双边滤波已应用，直径={diameter}, sigma_color={sigma_color}, sigma_space={sigma_space}。")
                # st.image(image_controller.get_current_image(), caption=f"双边滤波：直径={diameter}, sigma_color={sigma_color}, sigma_space={sigma_space}", use_container_width=True)

    if st.sidebar.checkbox("锐化（空域）"):
        if current_image is None:
            st.sidebar.info("请先上传一张图像以使用锐化操作。")
        else:
            sharpen_type = st.sidebar.selectbox("选择锐化算子",
                                                ["拉普拉斯算子", "Sobel算子", "自定义算子"])

            if sharpen_type == "拉普拉斯算子":
                alpha = st.sidebar.slider("增强因子 (alpha)", 0.0, 10.0, 1.0, 0.1)
                if st.sidebar.button("应用拉普拉斯锐化"):
                    image_controller.apply_operation(sharpen_filter, method="laplacian", alpha=alpha)
                    st.success(f"拉普拉斯锐化已应用，增强因子={alpha}。")

            elif sharpen_type == "Sobel算子":
                direction = st.sidebar.selectbox("方向", ["水平", "垂直", "综合"])
                if st.sidebar.button("应用Sobel锐化"):
                    image_controller.apply_operation(sharpen_filter, method="sobel", direction=direction)
                    st.success(f"Sobel锐化已应用，方向={direction}。")

            # elif sharpen_type == "高提升滤波":
            #     alpha = st.sidebar.slider("高提升因子 (alpha)", 1.0, 10.0, 1.5, 0.1)
            #     if st.sidebar.button("应用高提升滤波"):
            #         image_controller.apply_operation(sharpen_image, method="high_boost", alpha=alpha)
            #         st.success(f"高提升滤波已应用，alpha={alpha}。")

            elif sharpen_type == "自定义算子":
                kernel_size = st.sidebar.slider("自定义核大小", 3, 11, 3, 2)
                kernel_values = st.sidebar.text_area("输入核矩阵值（以逗号分隔）", "-1,-1,-1,-1,9,-1,-1,-1,-1")
                if st.sidebar.button("应用自定义锐化"):
                    kernel = np.array(list(map(float, kernel_values.split(",")))).reshape(kernel_size, kernel_size)
                    image_controller.apply_operation(sharpen_filter, method="custom", kernel=kernel)
                    st.success(f"自定义锐化已应用，核大小={kernel_size}。")

    if st.sidebar.checkbox("频域滤波"):
        if current_image is None:
            st.sidebar.info("请先上传一张图像以使用滤波与噪声操作。")
            return
        # 确保频域滤波选项仅在图像为灰度图时启用
        image_np = np.array(current_image)
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            st.sidebar.warning("频域滤波仅支持灰度图像。请先将图像转换为灰度图。")
        else:
            # 选择滤波类型：低通或高通
            pass_type = st.sidebar.selectbox("选择滤波类型", ["低通滤波", "高通滤波"])
            # 选择具体滤波器类型
            filter_type = st.sidebar.selectbox("选择滤波器", ["理想滤波器", "巴特沃斯滤波器", "高斯滤波器"])

            # 获取滤波参数
            cutoff = st.sidebar.slider("截止频率", 1, 500, 30, 1)
            if filter_type == "巴特沃斯滤波器":
                order = st.sidebar.slider("巴特沃斯阶数", 1, 10, 2, 1)
            else:
                order = 2  # Default value, not used

            if filter_type == "高斯滤波器":
                n = st.sidebar.slider("高斯标准差", 1, 100, 10, 1)
            else:
                n = 2  # Default value, not used

            filter_params = {"cutoff": cutoff, "order": order, "n": n}

            # 应用滤波
            if st.sidebar.button(f"应用{pass_type}滤波"):
                try:
                    filtered_image, f_image, f_image_filtered = apply_frequency_filter_to_image(
                        current_image,
                        filter_type=filter_type,#.lower().replace("滤波器", ""),
                        pass_type=pass_type,
                        cutoff=cutoff,
                        order=order,
                        n=n
                    )
                    image_controller.apply_operation(lambda _: filtered_image)
                    st.success(f"{pass_type}滤波已应用，参数={filter_params}。")

                    # 显示频域图像和滤波后的频域图像
                    st.subheader("频域图像")
                    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
                    ax[0].imshow(f_image, cmap='gray')
                    ax[0].set_title('original frequency image')
                    ax[0].axis('off')
                    ax[1].imshow(f_image_filtered, cmap='gray')
                    ax[1].set_title('filtered frequency image')
                    ax[1].axis('off')
                    st.pyplot(fig)
                except Exception as e:
                    st.sidebar.error(f"频域滤波失败: {e}")

    if st.sidebar.checkbox("同态滤波（频域）"):
        if current_image is None:
            st.sidebar.info("请先上传一张图像以使用同态滤波。")
        else:
            filter_type = st.sidebar.selectbox("选择滤波器", ["理想滤波器", "巴特沃斯滤波器", "高斯滤波器"], key="homomorphic_filter_type")
            low_cutoff = st.sidebar.slider("低频截止", 1.0, 30.0, 2.0, 0.1)
            high_cutoff = st.sidebar.slider("高频截止", 10.0, 100.0, 50.0, 1.0)
            alpha = st.sidebar.slider("低频增益 (alpha)", 0.0, 10.0, 1.0, 0.1)
            beta = st.sidebar.slider("高频增益 (beta)", 0.0, 50.0, 2.0, 0.1)

            if st.sidebar.button("应用同态滤波"):
                image_controller.apply_operation(
                    homomorphic_filter,
                    low_cutoff=low_cutoff,
                    high_cutoff=high_cutoff,
                    alpha=alpha,
                    beta=beta,
                    filter_type=filter_type
                )
                st.success(f"同态滤波已应用，滤波器={filter_type}, 参数: 低频增益={alpha}, 高频增益={beta}。")
