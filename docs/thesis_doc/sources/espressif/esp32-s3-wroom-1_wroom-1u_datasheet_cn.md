ESP32-S3-WROOM-1 ESP32-S3-WROOM-1U 技术规格书 版本 1.7

2.4 GHz Wi-Fi (802.11b/g/n) + 蓝牙 ® 5 模组 内置 ESP32-S3 系列芯片，Xtensa® 双核 32 位 LX7 处理器 Flash 最大可选 16 MB，PSRAM 最大可选 16 MB 最多 36 个 GPIO，丰富的外设 板载 PCB 天线或外部天线连接器

                ESP32-S3-WROOM-1                ESP32-S3-WROOM-1U




                                   www.espressif.com

1 模组概述

1 模组概述 说明：

点击链接或扫描二维码确保您使用的是最新版本的文档： https://www.espressif.com/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_cn.pdf

1.1 特性

CPU 和片上存储器 -- 4 个作为 strapping 管脚

                                                        • SPI、LCD、Camera 接口、UART、I2C、I2S、红

• 内置 ESP32-S3 系列芯片，Xtensa® 双核 32 位 外遥控、脉冲计数器、LED PWM、全速 USB 2.0 LX7 微处理器 (支持单精度浮点运算单元)，支持 OTG、USB 串口/JTAG 控制器、MCPWM、SD/ 高达 240 MHz 的时钟频率 MMC 主机控制器、GDMA、TWAI® 控制器（兼容 • 384 KB ROM ISO 11898-1）、ADC、触摸传感器、温度传感器、 • 512 KB SRAM 定时器和看门狗

• 16 KB RTC SRAM 模组集成元件 • 最大 16 MB PSRAM • 40 MHz 集成晶振

Wi-Fi • 最大 16 MB Quad SPI flash

• 802.11b/g/n 天线选型 • 802.11n 模式下数据速率高达 150 Mbps • ESP32-S3-WROOM-1：板载 PCB 天线 • 帧聚合 (TX/RX A-MPDU, TX/RX A-MSDU) • ESP32-S3-WROOM-1U：通过连接器连接外部天 • 0.4 µs 保护间隔 线

• 工作信道中心频率范围：2412 \~ 2484 MHz 工作条件 蓝牙 • 工作电压/供电电压：3.0 \~ 3.6 V

• 低功耗蓝牙 (Bluetooth LE)：Bluetooth 5、 • 工作环境温度： Bluetooth mesh -- 65 °C 版模组：--40 \~ 65 °C • 速率支持 125 Kbps、500 Kbps、1 Mbps、2 -- 85 °C 版模组：--40 \~ 85 °C Mbps -- 105 °C 版模组：--40 \~ 105 °C • 广播扩展 (Advertising Extensions)

• 多广播 (Multiple Advertisement Sets) 认证 • 信道选择 (Channel Selection Algorithm #2) • RF 认证：见 证书

• Wi-Fi 与蓝牙共存，共用同一个天线 • 环保认证：RoHS/REACH

外设 测试

• 36 个 GPIO • HTOL/HTSL/uHAST/TCT/ESD

乐鑫信息科技 2 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 1 模组概述

1.2 型号对比 ESP32-S3-WROOM-1 和 ESP32-S3-WROOM-1U 是两款通用型 Wi-Fi + 低功耗蓝牙 MCU 模组，搭载 ESP32-S3 系列芯片。除具有丰富的外设接口外，模组还拥有强大的神经网络运算能力和信号处理能力，适用于 AIoT 领域 的多种应用场景，例如唤醒词检测和语音命令识别、人脸检测和识别、智能家居、智能家电、智能控制面板、 智能扬声器等。

ESP32-S3-WROOM-1 采用 PCB 板载天线，ESP32-S3-WROOM-1U 采用连接器连接外部天线。两款模组均有多 种型号可供选择，具体见表 1-1 和 1-2。其中，ESP32-S3-WROOM-1-H4 和 ESP32-S3-WROOM-1U-H4 的工作环 境温度为--40 \~ 105 °C，内置 ESP32-S3R8 和 ESP32-S3R16V 的模组工作环境温度为--40 \~ 65 °C，其他型号的 工作环境温度均为--40 \~ 85 °C。请注意，针对 R8 和 R16V 系列模组 (内置 Octal SPI PSRAM)，若开启 PSRAM ECC 功能，模组最大环境温度可以提高到 85 °C，但是 PSRAM 的可用容量将减少 1/16。

                               表 1-1. ESP32-S3-WROOM-1 系列型号对比1

                                                                           环境温度5       模组尺寸6
      订购代码2                            Flash3, 4           PSRAM4
                                                                             (°C)       (mm)
      ESP32-S3-WROOM-1-N4           4 MB (Quad SPI)            -           –40 ~ 85
      ESP32-S3-WROOM-1-N8           8 MB (Quad SPI)            -           –40 ~ 85
      ESP32-S3-WROOM-1-N16          16 MB (Quad SPI)           -           –40 ~ 85
                                                                                        18.0
      ESP32-S3-WROOM-1-H4           4 MB (Quad SPI)            -           –40 ~ 105
                                                                                         ×
      ESP32-S3-WROOM-1-N4R2         4 MB (Quad SPI)    2 MB (Quad SPI)     –40 ~ 85
                                                                                        25.5
      ESP32-S3-WROOM-1-N8R2         8 MB (Quad SPI)    2 MB (Quad SPI)     –40 ~ 85
                                                                                         ×
      ESP32-S3-WROOM-1-N16R2        16 MB (Quad SPI)   2 MB (Quad SPI)     –40 ~ 85
                                                                                         3.1
      ESP32-S3-WROOM-1-N4R8         4 MB (Quad SPI)    8 MB (Octal SPI)    –40 ~ 65
      ESP32-S3-WROOM-1-N8R8         8 MB (Quad SPI)    8 MB (Octal SPI)    –40 ~ 65
      ESP32-S3-WROOM-1-N16R8        16 MB (Quad SPI)   8 MB (Octal SPI)    –40 ~ 65
      ESP32-S3-WROOM-1-N16R16VA7    16 MB (Quad SPI)   16 MB (Octal SPI)   –40 ~ 65
      1 本表格中的注释内容与表 1-2 一致。

                              表 1-2. ESP32-S3-WROOM-1U 系列型号对比

                                                                           环境温度5       模组尺寸6
      订购代码2                             Flash3, 4          PSRAM4
                                                                              (°C)      (mm)
      ESP32-S3-WROOM-1U-N4           4 MB (Quad SPI)           -            –40 ~ 85
      ESP32-S3-WROOM-1U-N8           8 MB (Quad SPI)           -            –40 ~ 85
      ESP32-S3-WROOM-1U-N16         16 MB (Quad SPI)           -            –40 ~ 85
                                                                                         18.0
      ESP32-S3-WROOM-1U-H4           4 MB (Quad SPI)           -           –40 ~ 105
                                                                                          ×
      ESP32-S3-WROOM-1U-N4R2         4 MB (Quad SPI)    2 MB (Quad SPI)     –40 ~ 85
                                                                                         19.2
      ESP32-S3-WROOM-1U-N8R2         8 MB (Quad SPI)    2 MB (Quad SPI)     –40 ~ 85
                                                                                          ×
      ESP32-S3-WROOM-1U-N16R2       16 MB (Quad SPI)    2 MB (Quad SPI)     –40 ~ 85
                                                                                         3.2
      ESP32-S3-WROOM-1U-N4R8         4 MB (Quad SPI)    8 MB (Octal SPI)    –40 ~ 65
      ESP32-S3-WROOM-1U-N8R8         8 MB (Quad SPI)    8 MB (Octal SPI)    –40 ~ 65
      ESP32-S3-WROOM-1U-N16R8       16 MB (Quad SPI)    8 MB (Octal SPI)    –40 ~ 65
      ESP32-S3-WROOM-1U-N16R16VA7   16 MB (Quad SPI)   16 MB (Octal SPI)    –40 ~ 65

乐鑫信息科技 3 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 1 模组概述

2 如需定制 ESP32-S3-WROOM-1-H4、ESP32-S3-WROOM-1U-H4 或 ESP32-S3-WROOM-1U-N16R16VA 模 组，请 联系我们。 3 默认情况下，模组 SPI flash 支持的最大时钟频率为 80 MHz，且不支持自动暂停功能。如需使用 120 MHz 的 flash 时钟频率或需要 flash 自动暂停功能，请 联系我们。 4 该模组使用封装在芯片中的 PSRAM。更多关于存储器规格的信息，请参考章节 6.5 存储器规格。 5 环境温度指乐鑫模组外部的推荐环境温度。 6 更多关于模组尺寸的信息，请参考章节 10.1 模组尺寸。 7 注意，仅 ESP32-S3-WROOM-1-N16R16VA 和 ESP32-S3-WROOM-1U-N16R16VA 的 VDD_SPI 电压为 1.8 V。

两款模组采用的是 ESP32-S3 系列芯片。ESP32-S3 系列芯片搭载 Xtensa® 32 位 LX7 双核处理器（支持单精度 浮点运算单元），工作频率高达 240 MHz。CPU 电源可被关闭，利用低功耗协处理器监测外设的状态变化或某 些模拟量是否超出阈值。

说明： 关于 ESP32-S3 的更多信息请参考 《ESP32-S3 系列芯片技术规格书》。 关于芯片版本识别、特定芯片版本的 ESP-IDF 支持版本以及其他芯片版本信息，请参考 《ESP32-S3 系列芯片勘误表》 \> 章节 芯片版本标识。

1.3 应用 • 智能家居 • 通用低功耗 IoT 传感器集线器

• 工业自动化 • 通用低功耗 IoT 数据记录器

• 医疗保健 • 摄像头视频流传输

• 消费电子产品 • USB 设备

• 智慧农业 • 语音识别

• POS 机 • 图像识别

• 服务机器人 • Wi-Fi + 蓝牙网卡

• 音频设备 • 触摸和接近感应

乐鑫信息科技 4 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 目录

目录

1 模组概述 2 1.1 特性 2 1.2 型号对比 3 1.3 应用 4

2 功能框图 9

3 管脚定义 10 3.1 管脚布局 10 3.2 管脚描述 11

4 启动配置项 13 4.1 芯片启动模式控制 14 4.2 VDD_SPI 电压控制 15 4.3 ROM 日志打印控制 15 4.4 JTAG 信号源控制 15 4.5 芯片上电和复位 16

5 外设 17 5.1 外设概述 17 5.2 外设描述 17 5.2.1 通讯接口 17 5.2.1.1 UART 控制器 17 5.2.1.2 I2C 接口 18 5.2.1.3 I2S 接口 19 5.2.1.4 LCD 与 Camera 控制器 19 5.2.1.5 串行外设接口 (SPI) 19 ® 5.2.1.6 双线汽车接口 (TWAI ) 21 5.2.1.7 USB 2.0 OTG 全速接口 22 5.2.1.8 USB 串口/JTAG 控制器 23 5.2.1.9 SD/MMC 主机控制器 24 5.2.1.10 LED PWM 控制器 25 5.2.1.11 电机控制脉宽调制器 (MCPWM) 25 5.2.1.12 红外遥控 (RMT) 25 5.2.1.13 脉冲计数控制器 (PCNT) 26 5.2.2 模拟信号处理 27 5.2.2.1 SAR ADC 27 5.2.2.2 温度传感器 27 5.2.2.3 触摸传感器 27

6 电气特性 28 6.1 绝对最大额定值 28 6.2 建议工作条件 28

乐鑫信息科技 5 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 目录

6.3 直流电气特性 (3.3 V, 25 °C) 28 6.4 功耗特性 29 6.4.1 Active 模式下的功耗 29 6.4.2 其他功耗模式下的功耗 29 6.5 存储器规格 30

7 射频特性 32 7.1 Wi-Fi 射频 32 7.1.1 Wi-Fi 射频发射器 (TX) 特性 32 7.1.2 Wi-Fi 射频接收器 (RX) 特性 33 7.2 低功耗蓝牙射频 34 7.2.1 低功耗蓝牙射频发射器 (TX) 特性 34 7.2.2 低功耗蓝牙射频接收器 (RX) 特性 36

8 模组原理图 39

9 外围设计原理图 41

10 尺寸规格 42 10.1 模组尺寸 42 10.2 外部天线连接器尺寸 43

11 PCB 布局建议 45 11.1 PCB 封装图形 45 11.2 PCB 设计中的模组位置摆放 46

12 产品处理 47 12.1 存储条件 47 12.2 静电放电 (ESD) 47 12.3 回流焊温度曲线 47 12.4 超声波振动 48

技术规格书版本号管理 49

相关文档和资源 50

修订历史 51

乐鑫信息科技 6 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 表格

表格 1-1 ESP32-S3-WROOM-1 系列型号对比1 3 1-2 ESP32-S3-WROOM-1U 系列型号对比 3 3-1 管脚定义 11 4-1 Strapping 管脚的默认配置 13 4-2 Strapping 管脚的时序参数说明 14 4-3 芯片启动模式控制 14 4-4 VDD_SPI 电压控制 15 4-5 JTAG 信号源控制 15 4-6 上电和复位时序参数说明 16 6-1 绝对最大额定值 28 6-2 建议工作条件 28 6-3 直流电气特性 (3.3 V, 25 °C) 28 6-4 Active 模式下 Wi-Fi (2.4 GHz) 功耗特性 29 6-5 Active 模式下低功耗蓝牙功耗特性 29 6-6 Modem-sleep 模式下的功耗 30 6-7 低功耗模式下的功耗 30 6-8 Flash 规格 31 6-9 PSRAM 规格 31 7-1 Wi-Fi 射频规格 32 7-2 频谱模板和 EVM 符合 802.11 标准时的发射功率 32 7-3 发射 EVM 测试1 32 7-4 接收灵敏度 33 7-5 最大接收电平 34 7-6 接收邻道抑制 34 7-7 低功耗蓝牙射频规格 34 7-8 低功耗蓝牙 - 发射器特性 - 1 Mbps 34 7-9 低功耗蓝牙 - 发射器特性 - 2 Mbps 35 7-10 低功耗蓝牙 - 发射器特性 - 125 Kbps 35 7-11 低功耗蓝牙 - 发射器特性 - 500 Kbps 35 7-12 低功耗蓝牙 - 接收器特性 - 1 Mbps 36 7-13 低功耗蓝牙 - 接收器特性 - 2 Mbps 36 7-14 低功耗蓝牙 - 接收器特性 - 125 Kbps 37 7-15 低功耗蓝牙 - 接收器特性 - 500 Kbps 37

乐鑫信息科技 7 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 插图

插图 2-1 ESP32-S3-WROOM-1 功能框图 9 2-2 ESP32-S3-WROOM-1U 功能框图 9 3-1 管脚布局（顶视图） 10 4-1 Strapping 管脚的时序参数图 14 4-2 上电和复位时序参数图 16 8-1 ESP32-S3-WROOM-1 原理图 39 8-2 ESP32-S3-WROOM-1U 原理图 40 9-1 外围设计原理图 41 10-1 ESP32-S3-WROOM-1 模组尺寸 42 10-2 ESP32-S3-WROOM-1U 模组尺寸 42 10-3 外部天线连接器尺寸图 43 11-1 ESP32-S3-WROOM-1 推荐 PCB 封装图 45 11-2 ESP32-S3-WROOM-1U 推荐 PCB 封装图 46 12-1 回流焊温度曲线 47

乐鑫信息科技 8 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见  QSPI Flash 2 功能框图

2 功能框图

                                                  ESP32-S3-WROOM-1
                                40 MHz
          3V3                   Crystal                             Antenna


                             ESP32-S3
                             ESP32-S3R2              RF Matching
                             ESP32-S3R8
                     EN      ESP32-S3R16V                 GPIOs
                                    PSRAM(opt.)
                                    (QSPI/OSPI)




                             VDD_SPI
                             SPICS0
                             SPICLK




                             SPIWP
                             SPIHD
                             SPIQ
                             SPID



                               QSPI Flash



                          图 2-1. ESP32-S3-WROOM-1 功能框图




                                                  ESP32-S3-WROOM-1U
                                 40 MHz
          3V3                    Crystal                                      Antenna


                             ESP32-S3
                             ESP32-S3R2               RF Matching
                             ESP32-S3R8
                     EN      ESP32-S3R16V                 GPIOs
                                    PSRAM(opt.)
                                    (QSPI/OSPI)
                              VDD_SPI
                              SPICS0
                              SPICLK




                              SPIWP
                              SPIHD
                              SPIQ
                              SPID




                               QSPI Flash



                          图 2-2. ESP32-S3-WROOM-1U 功能框图

    说明：
    关于芯片与封装内 PSRAM 的管脚对应关系，请参考 《ESP32-S3 系列芯片技术规格书》 > 表格 芯片与封装内 flash/
    PSRAM 的管脚对应关系。
                                                  ESP32-S3-WROOM-1
                                40 MHz
          3V3                   Crystal                             Antenna


                             ESP32-S3
                             ESP32-S3R2              RF Matching
                             ESP32-S3R8
                     EN      ESP32-S3R16V                 GPIOs
                                    PSRAM(opt.)
                                    (QSPI/OSPI)
                             VDD_SPI
                             SPICS0
                             SPICLK




                             SPIWP
                             SPIHD
                             SPIQ
                             SPID

乐鑫信息科技 9 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 QSPI Flash 3 管脚定义

3 管脚定义

3.1 管脚布局 管脚布局图显示了模组上管脚的大致位置。按比例绘制的实际布局请参考图 10.1 模组尺寸。

                                                    Keepout Zone




            GND    1                                                                                             40   GND

            3V3    2                                                                                             39   IO1

             EN    3                                                                                             38   IO2

             IO4   4                                                                                             37   TXD0

             IO5   5                                                                                             36   RXD0

             IO6   6                        GND     GND      GND                                                 35   IO42

             IO7   7                        GND
                                                     41
                                                    GND
                                                             GND                                                 34   IO41

            IO15   8                        GND     GND      GND                                                 33   IO40

            IO16   9                                                                                             32   IO39

            IO17   10                                                                                            31   IO38

            IO18   11                                                                                            30   IO37

             IO8   12                                                                                            29   IO36

            IO19   13                                                                                            28   IO35

            IO20   14                                                                                            27   IO0
                                                                      21

                                                                             22
                                                          20




                                                                                    23

                                                                                            24



                                                                                                          26
                                                                                                   25
                              16

                                     17

                                           18

                                                  19
                        15




                                                  IO11




                                                                                    IO21
                                                          IO12
                                           IO10




                                                                             IO14
                        IO3

                              IO46




                                                                      IO13




                                                                                            IO47
                                     IO9




                                                                                                   IO48

                                                                                                          IO45




                                           图 3-1. 管脚布局（顶视图）



    说明 A：
    虚线标记区域为天线净空区。ESP32-S3-WROOM-1U 的管脚布局与 ESP32-S3-WROOM-1 相同，但没有天线净空区。
    关于底板上模组天线净空区的更多信息，请查看 《ESP32-S3 硬件设计指南》 > 章节 基于模组的版图设计通用要点。

乐鑫信息科技 10 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 3 管脚定义

3.2 管脚描述 模组共有 41 个管脚，具体描述参见表 3-1 管脚定义。

管脚名称释义、管脚功能释义、以及外设管脚分配请参考 《ESP32-S3 系列芯片技术规格书》。

                                        表 3-1. 管脚定义

      名称       序号   类型 a    功能
      GND      1     P      接地
      3V3      2     P      供电
                            高电平：芯片使能；
      EN       3      I     低电平：芯片关闭；
                            注意不能让 EN 管脚浮空。
      IO4      4    I/O/T   RTC_GPIO4, GPIO4, TOUCH4, ADC1_CH3
      IO5      5    I/O/T   RTC_GPIO5, GPIO5, TOUCH5, ADC1_CH4
      IO6      6    I/O/T   RTC_GPIO6, GPIO6, TOUCH6, ADC1_CH5
      IO7      7    I/O/T   RTC_GPIO7, GPIO7, TOUCH7, ADC1_CH6
      IO15     8    I/O/T   RTC_GPIO15, GPIO15, U0RTS, ADC2_CH4, XTAL_32K_P
      IO16     9    I/O/T   RTC_GPIO16, GPIO16, U0CTS, ADC2_CH5, XTAL_32K_N
      IO17     10   I/O/T   RTC_GPIO17, GPIO17, U1TXD, ADC2_CH6
      IO18     11   I/O/T   RTC_GPIO18, GPIO18, U1RXD, ADC2_CH7, CLK_OUT3
      IO8      12   I/O/T   RTC_GPIO8, GPIO8, TOUCH8, ADC1_CH7, SUBSPICS1
      IO19     13   I/O/T   RTC_GPIO19, GPIO19, U1RTS, ADC2_CH8, CLK_OUT2, USB_D-
      IO20     14   I/O/T   RTC_GPIO20, GPIO20, U1CTS, ADC2_CH9, CLK_OUT1, USB_D+
      IO3      15   I/O/T   RTC_GPIO3, GPIO3, TOUCH3, ADC1_CH2
      IO46     16   I/O/T   GPIO46
      IO9      17   I/O/T   RTC_GPIO9, GPIO9, TOUCH9, ADC1_CH8, FSPIHD, SUBSPIHD
                            RTC_GPIO10, GPIO10, TOUCH10, ADC1_CH9, FSPICS0, FSPIIO4,
      IO10     18   I/O/T
                            SUBSPICS0
      IO11     19   I/O/T   RTC_GPIO11, GPIO11, TOUCH11, ADC2_CH0, FSPID, FSPIIO5, SUBSPID
                            RTC_GPIO12, GPIO12, TOUCH12, ADC2_CH1, FSPICLK, FSPIIO6,
      IO12     20   I/O/T
                            SUBSPICLK
      IO13     21   I/O/T   RTC_GPIO13, GPIO13, TOUCH13, ADC2_CH2, FSPIQ, FSPIIO7, SUBSPIQ
                            RTC_GPIO14, GPIO14, TOUCH14, ADC2_CH3, FSPIWP, FSPIDQS,
      IO14     22   I/O/T
                            SUBSPIWP
      IO21     23   I/O/T   RTC_GPIO21, GPIO21
      IO47 c   24   I/O/T   SPICLK_P_DIFF, GPIO47, SUBSPICLK_P_DIFF
      IO48 c   25   I/O/T   SPICLK_N_DIFF, GPIO48, SUBSPICLK_N_DIFF
      IO45     26   I/O/T   GPIO45
      IO0      27   I/O/T   RTC_GPIO0, GPIO0
      IO35 b   28   I/O/T   SPIIO6, GPIO35, FSPID, SUBSPID
      IO36 b   29   I/O/T   SPIIO7, GPIO36, FSPICLK, SUBSPICLK
      IO37 b   30   I/O/T   SPIDQS, GPIO37, FSPIQ, SUBSPIQ
      IO38     31   I/O/T   GPIO38, FSPIWP, SUBSPIWP
                                                                                       见下页

乐鑫信息科技 11 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 3 管脚定义

                                   表 3-1 – 接上页

名称 序号 类型 a 功能 IO39 32 I/O/T MTCK, GPIO39, CLK_OUT3, SUBSPICS1 IO40 33 I/O/T MTDO, GPIO40, CLK_OUT2 IO41 34 I/O/T MTDI, GPIO41, CLK_OUT1 IO42 35 I/O/T MTMS, GPIO42 RXD0 36 I/O/T U0RXD, GPIO44, CLK_OUT2 TXD0 37 I/O/T U0TXD, GPIO43, CLK_OUT1 IO2 38 I/O/T RTC_GPIO2, GPIO2, TOUCH2, ADC1_CH1 IO1 39 I/O/T RTC_GPIO1, GPIO1, TOUCH1, ADC1_CH0 GND 40 P 接地 EPAD 41 P 接地 a P：电源；I：输入；O：输出；T：可设置为高阻。加粗字体为管脚的默认功能。管脚 28 ∼ 30 的默 认功能由 eFuse 位决定。 b 在集成 Octal SPI PSRAM（即内置芯片为 ESP32-S3R8 或 ESP32-S3R16V）的模组中，管脚 IO35、 IO36、IO37 已连接至模组内部集成的 Octal SPI PSRAM，不可用于其他功能。 c 在内置芯片为 ESP32-S3R16V 的模组中，由于 ESP32-S3R16V 芯片的 VDD_SPI 电压已设置为 1.8 V，所以，不同于其他 GPIO，VDD_SPI 电源域中的 GPIO47 和 GPIO48 工作电压也为 1.8 V。

乐鑫信息科技 12 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 4 启动配置项

4 启动配置项 说明： 以下内容摘自 《ESP32-S3 系列芯片技术规格书》 \> 章节 启动配置项。芯片 Strapping 管脚与模组管脚的对应关系，可 参考章节 8 模组原理图。

芯片在上电或硬件复位时，可以通过 Strapping 管脚和 eFuse 位配置如下启动参数，无需微处理器的参 与：

• 芯片启动模式

     – Strapping 管脚：GPIO0 和 GPIO46

• VDD_SPI 电压

     – Strapping 管脚：GPIO45

     – eFuse 参数：EFUSE_VDD_SPI_FORCE 和 EFUSE_VDD_SPI_TIEH

• ROM 日志打印

     – Strapping 管脚：GPIO46

     – eFuse 参数：EFUSE_UART_PRINT_CONTROL 和 EFUSE_DIS_USB_SERIAL_JTAG_ROM_PRINT

• JTAG 信号源

     – Strapping 管脚：GPIO3

     – eFuse 参数：EFUSE_DIS_PAD_JTAG、EFUSE_DIS_USB_JTAG 和 EFUSE_STRAP_JTAG_SEL

上述 eFuse 参数的默认值均为 0，也就是说没有烧写过。eFuse 只能烧写一次，一旦烧写为 1，便不能恢复为 0。有关烧写 eFuse 的信息，请参考 《ESP32-S3 技术参考手册》 \> 章节 eFuse 控制器。

上述 strapping 管脚如果没有连接任何电路或连接的电路处于高阻抗状态，则其默认值（即逻辑电平值）取决于 管脚内部弱上拉/下拉电阻在复位时的状态。

                             表 4-1. Strapping 管脚的默认配置

                             Strapping 管脚        默认配置   值
                             GPIO0               弱上拉    1
                             GPIO3               浮空     –
                             GPIO45              弱下拉    0
                             GPIO46              弱下拉    0

要改变 strapping 管脚的值，可以连接外部下拉/上拉电阻。如果 ESP32-S3 用作主机 MCU 的从设备， strapping 管脚的电平也可通过主机 MCU 控制。

所有 strapping 管脚都有锁存器。系统复位时，锁存器采样并存储相应 strapping 管脚的值，一直保持到芯片掉 电或关闭。锁存器的状态无法用其他方式更改。因此，strapping 管脚的值在芯片工作时一直可读取，strapping 管脚在芯片复位后作为普通 IO 管脚使用。

Strapping 管脚的信号时序需遵循表 4-2 和图 4-1 所示的 建立时间和 保持时间。

乐鑫信息科技 13 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 4 启动配置项

                                    表 4-2. Strapping 管脚的时序参数说明

        参数    说明                                                                     最小值 (ms)
        tSU   建立时间，即拉高 EN 激活芯片前，电源轨达到稳定所需的时间                                                   0
              保持时间，即 EN 已拉高、strapping 管脚变为普通 IO 管脚开始工
        tH                                                                                     3
              作前，可读取 strapping 管脚值的时间


                                                tSU         tH




                               VIL_nRST
                        EN




                                  VIH



               Strapping pin


                                        图 4-1. Strapping 管脚的时序参数图

4.1 芯片启动模式控制 复位释放后，GPIO0 和 GPIO46 共同决定启动模式。详见表 4-3 芯片启动模式控制。

                                            表 4-3. 芯片启动模式控制

                                启动模式                        GPIO0    GPIO46
                                SPI Boot                         1   任意值
                                Joint Download Boot 2         0        0
                                 1 加粗表示默认值和默认配置。
                                 2 Joint Download Boot 模式下支持以下下载
                                   方式：
                                          • USB Download Boot：
                                             – USB-Serial-JTAG Download Boot
                                             – USB-OTG Download Boot
                                          • UART Download Boot

在 SPI Boot 模式下，ROM 引导加载程序通过从 SPI flash 中读取程序来启动系统。

在 Joint Download Boot 模式下，用户可通过 USB 或 UART0 接口将二进制文件下载至 flash，或将二进制文件 下载至 SRAM 并运行 SRAM 中的程序。

除了 SPI Boot 和 Joint Download Boot 模式，ESP32-S3 还支持 SPI Download Boot 模式，详见 《ESP32-S3 技术参考手册》 \> 章节 芯片 Boot 控制。

乐鑫信息科技 14 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 4 启动配置项

4.2 VDD_SPI 电压控制 电压有两种控制方式，具体取决于 EFUSE_VDD_SPI_FORCE 的值。

                                        表 4-4. VDD_SPI 电压控制

VDD_SPI 电源 2 电压 EFUSE_VDD_SPI_FORCE GPIO45 EFUSE_VDD_SPI_TIEH VDD3P3_RTC 通过 RSP I 供电 3.3 V 0 0 忽略 Flash 稳压器 1.8 V 1 Flash 稳压器 1.8 V 0 1 忽略 VDD3P3_RTC 通过 RSP I 供电 3.3 V 1 1 加粗表示默认值和默认配置。 2 请参考章节 《ESP32-S3 系列芯片技术规格书》 \> 章节 电源管理。

4.3 ROM 日志打印控制 系统启动过程中，ROM 代码日志可打印至：

•（默认）UART0 和 USB 串口/JTAG 控制器

• USB 串口/JTAG 控制器

• UART0

通过配置寄存器和 eFuse 可分别关闭 UART 和 USB 串口/JTAG 控制器的 ROM 代码日志打印功能。详细信息请 参考 《ESP32-S3 技术参考手册》 \> 章节 芯片 Boot 控制。

4.4 JTAG 信号源控制 在系统启动早期阶段，GPIO3 可用于控制 JTAG 信号源。该管脚没有内部上下拉电阻，strapping 的值必须由不 处于高阻抗状态的外部电路控制。

如表 4-5 所示，GPIO3 与 EFUSE_DIS_PAD_JTAG、EFUSE_DIS_USB_JTAG 和 EFUSE_STRAP_JTAG_SEL 共同 控制 JTAG 信号源。

                                        表 4-5. JTAG 信号源控制

JTAG 信号源 EFUSE_DIS_PAD_JTAG EFUSE_DIS_USB_JTAG EFUSE_STRAP_JTAG_SEL GPIO3 0 0 0 忽略 USB 串口/JTAG 控制器 0 0 1 1 1 0 忽略 忽略 0 0 1 0 JTAG 管脚 2 0 1 忽略 忽略 JTAG 关闭 1 1 忽略 忽略 1 加粗表示默认值和默认配置。 2 即 MTDI、MTCK、MTMS 和 MTDO。

乐鑫信息科技 15 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 4 启动配置项

4.5 芯片上电和复位 芯片上电后，其电源轨需要一点时间方可稳定。之后，用于上电和复位的管脚 EN 拉高，激活芯片。更多关于 EN 及上电和复位时序的信息，请见图 4-2 和表 4-6。

                                   tST BL                  tRST

                        2.8 V
          VDDA,
        VDD3P3,
    VDD3P3_RTC,
    VDD3P3_CPU

                        VIL_nRST
              EN



                                   图 4-2. 上电和复位时序参数图



                                   表 4-6. 上电和复位时序参数说明

       参数          说明                                                 最小值 (µs)
                   EN 管脚拉高激活芯片前，VDDA、VDD3P3、VDD3P3_RTC 和
       tST BL                                                                 50
                   VDD3P3_CPU 达到稳定所需的时间
                   EN 电平低于 VIL_nRST（具体数值参考表 6-3）从而复位芯片的时
       tRST                                                                   50
                   间

乐鑫信息科技 16 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

5 外设

5.1 外设概述 ESP32-S3 集成了丰富的外设，包括 SPI、LCD、Camera 接口、UART、I2C、I2S、红外遥控、脉冲计数器、LED PWM、USB 串口/JTAG、MCPWM、SD/MMC 主机控制器、TWAI® 控制器（兼容 ISO 11898-1，即 CAN 规范 、ADC、触摸传感器和温度传感器。此外，ESP32-S3 还有一个全速 USB 2.0 On-The-Go (OTG) 接口用于 2.0） USB 通讯。

关于模组外设的详细信息，请参考《ESP32-S3 系列芯片技术规格书》 \> 章节 功能描述。

说明： 以下内容出自 《ESP32-S3 系列芯片技术规格书》 \> 章节 外设。并非所有 IO 信号都在模组上引出，因此这些信息不完 全适用于 ESP32-S3-WROOM-1 以及 ESP32-S3-WROOM-1U。 关于外设信号的更多信息，可参考《ESP32-S3 技术参考手册》 \> 章节 GPIO 交换矩阵外设信号列表。

5.2 外设描述 本章节介绍了芯片上的外设接口，包括扩展芯片功能的通信接口和片上传感器。

5.2.1 通讯接口 本章节介绍了芯片与外部设备和网络进行通信和交互的接口。

5.2.1.1 UART 控制器

ESP32-S3 有三个 UART（通用异步收发器）控制器，即 UART0、UART1、UART2，支持异步通信（RS232 和 RS485）和 IrDA，通信速率可达到 5 Mbps。

特性

• 支持三个可预分频的时钟源

• 可编程收发波特率

• 三个 UART 的发送 FIFO 以及接收 FIFO 共享 1024 x 8-bit RAM

• 全双工异步通信

• 支持输入信号波特率自检功能

• 支持 5/6/7/8 位数据长度

• 支持 1/1.5/2/3 个停止位

• 支持奇偶校验位

• 支持 AT_CMD 特殊字符检测

• 支持 RS485 协议

• 支持 IrDA 协议

• 支持 GDMA 高速数据通信

乐鑫信息科技 17 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

• 支持 UART 唤醒模式

• 支持软件流控和硬件流控

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 UART 控制器。

管脚分配

• UART0

          – 连接发送和接收信号的管脚 U0TXD 和 U0RXD 通过 IO MUX 与 GPIO43 ~ GPIO44 复用，也可以通过
           GPIO 交换矩阵连接到任意 GPIO。

          – 硬件流控管脚 U0RTS 和 U0CTS 通过 IO MUX 与 GPIO15 ~ GPIO16、RTC_GPIO15 ~ RTC_GPIO16、
           XTAL_32K_P 和 XTAL_32K_N、SAR ADC2 管脚复用，也可以通过 GPIO 交换矩阵连接到任意 GPIO。

          – 硬件流控管脚 U0DTR 和 U0DSR 可以为任意 GPIO，通过 GPIO 交换矩阵配置。

• UART1

          – 连接发送和接收信号的管脚 U1TXD 和 U1RXD 通过 IO MUX 与 GPIO17 ~ GPIO18、RTC_GPIO17 ~
           RTC_GPIO18、SAR ADC2 管脚复用，也可以通过 GPIO 交换矩阵连接到任意 GPIO。

          – 硬件流控管脚 U1RTS 和 U1CTS 通过 IO MUX 与 GPIO19 ~ GPIO20、RTC_GPIO19 ~ RTC_GPIO20、
           USB_D- 和 USB_D+、以及 SAR ADC2 接口复用，也可以通过 GPIO 交换矩阵连接到任意 GPIO。

          – 硬件流控管脚 U1DTR 和 U1DSR 可以为任意 GPIO，通过 GPIO 交换矩阵配置。

• UART2：可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.2 I2C 接口

ESP32-S3 有两个 I2C 总线接口，根据用户的配置，总线接口可以用作 I2C 主机或从机模式。

特性

• 标准模式 (100 Kbit/s)

• 快速模式 (400 Kbit/s)

• 速度最高可达 800 Kbit/s，但受制于 SCL 和 SDA 上拉强度

• 7 位寻址模式和 10 位寻址模式

• 双地址（从机地址和从机寄存器地址）寻址模式

用户可以通过 I2C 硬件提供的指令抽象层更方便地控制 I2C 接口。

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 I2C 控制器。

管脚分配

I2C 的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

乐鑫信息科技 18 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

5.2.1.3 I2S 接口

ESP32-S3 有两个标准 I2S 接口，可以以主机或从机模式，在全双工或半双工模式下工作，并且可被配置为 I2S 串行 8/16/24/32 位的收发数据模式，支持频率从 10 kHz 到 40 MHz 的 BCK 时钟。

I2S 接口有专用的 DMA 控制器。支持 TDM PCM、TDM MSB 对齐、TDM LSB 对齐、TDM Phillips、PDM 接 口。

管脚分配

I2S 的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.4 LCD 与 Camera 控制器

ESP32-S3 的 LCD 与 Camera 控制器包含独立的 LCD 模块和 Camera 模块。

LCD 模块用于发送并行视频数据信号，其总线 8 位 \~ 16 位并行 RGB、I8080、MOTO6800 接口，支持的时钟频 率小于 40 MHz。支持 RGB565、YUV422、YUV420、YUV411 之间的互相转换。

Camera 模块用于接收并行视频数据信号，其总线支持 8 位 \~ 16 位 DVP 图像传感器接口，支持的时钟频率小于 40 MHz。支持 RGB565、YUV422、YUV420、YUV411 之间的互相转换。

管脚分配

LCD 与 Camera 控制器的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.5 串行外设接口 (SPI)

ESP32-S3 具有以下 SPI 接口：

• SPI0，供 ESP32-S3 的 GDMA 控制器与 Cache 访问封装内或封装外 flash/PSRAM

• SPI1，供 CPU 访问封装内或封装外 flash/PSRAM

• SPI2，通用 SPI 控制器，通过 GDMA 分配 DMA 通道进行访问

• SPI3，通用 SPI 控制器，通过 GDMA 分配 DMA 通道进行访问

特性

• SPI0 和 SPI1：

          – 支持 SPI、Dual SPI、Quad SPI、Octal SPI、QPI 和 OPI 模式

          – 八线 SPI 模式支持单倍数据速率 (SDR) 和双倍数据速率 (DDR)

          – 时钟频率可配置，八线 SPI SDR/DDR 模式下最高可达 120 MHz

          – 数据传输以字节为单位

• SPI2：

乐鑫信息科技 19 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

       – 支持主机或从机模式

       – 通过 GDMA 分配 DMA 通道进行访问

       – 支持 SPI、Dual SPI、Quad SPI、Octal SPI、QPI 和 OPI 模式

       – 时钟极性 (CPOL) 和相位 (CPHA) 可配置

       – 时钟频率可配置

       – 数据传输以字节为单位

       – 读写数据位序可配置：最高有效位 (MSB) 优先，或最低有效位 (LSB) 优先

       – 主机模式

           * 支持双线全双工通信，时钟频率最高可达 80 MHz

           * 八线 SPI 全双工模式仅支持单倍数据速率 (SDR)

           * 支持单线、双线、四线和八线半双工通信，时钟频率最高可达 80 MHz

           * 八线 SPI 半双工模式支持单倍数据速率（最高 80 MHz）和双倍数据速率（最高 40 MHz）

           * 具有六个 SPI_CS 管脚，可与六个独立 SPI 从机相连

           * CS 建立和保持时间可配置

       – 从机模式

           * 支持双线全双工通信，时钟频率最高可达 60 MHz

           * 支持单线、双线和四线半双工通信，时钟频率最高可达 60 MHz

           * 八线 SPI 全双工和半双工模式仅支持单倍数据速率 (SDR)

• SPI3：

       – 支持主机或从机模式

       – 通过 GDMA 分配 DMA 通道进行访问

       – 支持 SPI、Dual SPI、Quad SPI 和 QPI 模式

       – 时钟极性 (CPOL) 和相位 (CPHA) 可配置

       – 时钟频率可配置

       – 数据传输以字节为单位

       – 读写数据位序可配置：最高有效位 (MSB) 优先，或最低有效位 (LSB) 优先

       – 主机模式

           * 支持双线全双工通信，时钟频率最高可达 80 MHz

           * 支持单线、双线和四线半双工通信，时钟频率最高可达 80 MHz

           * 具有三个 SPI_CS 管脚，可与三个独立 SPI 从机相连

           * CS 建立和保持时间可配置

       – 从机模式

           * 支持双线全双工通信，时钟频率最高可达 60 MHz

乐鑫信息科技 20 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

             * 支持单线、双线和四线半双工通信，时钟频率最高可达 60 MHz

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 SPI 控制器。

管脚配置

说明： 请对照 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO MUX 功能 \> 表 IO MUX 管脚功能，参考以下 SPI 接口信息。

• SPI0/1

       – 通过 IO MUX：

             * 接口 4a，通过 IO MUX 与 GPIO26 ~ GPIO32 复用，与 4b 搭配使用在八线 SPI 模式下可作为低 4
              位数据线接口及 CLK、CS0、CS1 接口。

             * 接口 4b，通过 IO MUX 与 GPIO33 ~ GPIO37、SPI 接口 4e 和 4f 复用，与 4a 搭配使用在八线
              SPI 模式下可作为高 4 位数据线接口及 DQS 接口。

             * 接口 4d，通过 IO MUX 与 GPIO8 ~ GPIO14、RTC_GPIO8 ~ RTC_GPIO14、触摸传感器接口、SAR
              ADC 接口、以及 SPI 接口 4c 和 4g 复用。注意，不可使用 SPI2 接口连接。

             * 接口 4e，通过 IO MUX 与 GPIO33 ~ GPIO39、JTAG MTCK 接口、SPI 接口 4b 和 4f 复用，可在
              SPI0/1 非八线连接时使用。

       – 经 GPIO 交换矩阵：SPI0/1 的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

• SPI2

       – 通过 IO MUX：

             * 接口 4c，通过 IO MUX 与 GPIO9 ~ GPIO14、RTC_GPIO9 ~ RTC_GPIO14、触摸传感器接口、SAR
              ADC 接口、以及 SPI 接口 4d 和 4g 复用，用于快速 SPI 传输的 SPI2 主接口。

             *（不推荐使用）接口 4f，通过 IO MUX 与 GPIO33 ~ GPIO38、SPI 接口 4e 和 4b 复用，SPI2 主接
              口不可使用时的替代 SPI2 接口，其性能与通过 GPIO 交换矩阵使用 SPI2 类似，因此建议使用
              GPIO 交换矩阵。

             *（不推荐使用）接口 4g，通过 IO MUX 与 GPIO10 ~ GPIO14、RTC_GPIO10 ~ RTC_GPIO14、触摸传
              感器接口、SAR ADC 接口、以及 SPI 接口 4c 和 4d 复用，八线 SPI 连接的 SPI2 接口替代信号线。

       – 经 GPIO 交换矩阵：SPI2 的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

• SPI3：通过 GPIO 交换矩阵可配置使用任意 GPIO 管脚。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.6 双线汽车接口 (TWAI® )

双线汽车接口 (Two-Wire Automotive Interface, TWAI® ) 协议是一种多主机、多播的通信协议，具有检测错误、 发送错误信号以及内置报文优先仲裁等功能。ESP32-S3 带有一个 TWAI 控制器。

特性

• 兼容 ISO 11898-1 协议（CAN 规范 2.0）

• 标准帧格式（11 位 ID）和扩展帧格式（29 位 ID）

乐鑫信息科技 21 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

• 1 Kbit/s 到 1 Mbit/s 比特率

• 多种操作模式：

       – 工作模式

       – 监听模式

       – 自检模式（传输无需确认）

• 64 字节接收 FIFO

• 数据接收过滤器（支持单过滤器和双过滤器模式）

• 错误检测与处理：

       – 错误计数器

       – 可配置的错误中断阈值

       – 错误代码记录

       – 仲裁丢失记录

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 双线汽车接口。

管脚分配

TWAI 的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.7 USB 2.0 OTG 全速接口

ESP32-S3 带有一个集成了收发器的全速 USB OTG 外设，符合 USB 2.0 规范。

通用特性

• 支持全速和低速速率

• 主机协商协议 (HNP) 和会话请求协议 (SRP)，均可作为 A 或 B 设备

• 动态 FIFO (DFIFO) 大小

• 支持多种存储器访问模式

       – Scatter/Gather DMA 模式

       – 缓冲 (Buffer) DMA 模式

       – Slave 模式

• 可选择集成收发器或外部收发器

• 当仅使用集成收发器时，可通过时分复用技术，和 USB 串口/JTAG 控制器共用集成收发器

• 当集成收发器和外部收发器同时投入使用时，支持 USB OTG 和 USB 串口/JTAG 控制器两外设各自挑选不 同的收发器使用

乐鑫信息科技 22 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

设备模式 (Device mode) 特性

• 端点 0 永远存在（双向控制，由 EP0 IN 和 EP0 OUT 组成）

• 6 个附加端点 (1 \~ 6)，可配置为 IN 或 OUT

• 最多 5 个 IN 端点同时工作（包括 EP0 IN）

• 所有 OUT 端点共享一个 RX FIFO

• 每个 IN 端点都有专用的 TX FIFO

主机模式 (Host mode) 特性

• 8 个通道（管道）

       – 由 IN 与 OUT 两个通道组成的一个控制管道，因为 IN 和 OUT 必须分开处理。仅支持控制传输类型。

       – 其余 7 个管道可被配置为 IN 或 OUT，支持批量、同步、中断中的任意传输类型。

• 所有通道共用一个 RX FIFO、一个非周期性 TX FIFO、和一个周期性 TX FIFO。每个 FIFO 大小可配置。

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 USB OTG。

管脚分配

使用内部集成 PHY 时，USB OTG 的差分信号管脚 USB_D- 和 USB_D+ 通过 IO MUX 与 GPIO19 \~ GPIO20、 RTC_GPIO19 \~ RTC_GPIO20、UART1 接口和 SAR ADC2 接口复用。

使用外接 PHY 时，USB OTG 的管脚通过 IO MUX 与 GPIO21、RTC_GPIO21、GPIO38 \~ GPIO42 和 SPI 接口复 用：

• VP 信号连接到 MTMS 管脚

• VM 信号连接到 MTDI 管脚

• RCV 信号连接到 GPIO21 管脚

• OEN 信号连接到 MTDO 管脚

• VPO 信号连接到 MTCK 管脚

• VMO 信号连接到 GPIO38 管脚

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.8 USB 串口/JTAG 控制器

ESP32-S3 集成了一个 USB 串口/JTAG 控制器。

特性

• USB 全速标准

• 可配置为使用 ESP32-S3 内部 USB PHY 或通过 GPIO 交换矩阵使用外部 PHY

• 固定功能。包含连接的 CDC-ACM（通信设备类抽象控制模型）和 JTAG 适配器功能

• 共 2 个 OUT 端点、3 个 IN 端点和 1 个控制端点 EP_0，可实现最大 64 字节的数据载荷

乐鑫信息科技 23 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

• 包含内部 PHY，基本无需其他外部组件连接主机计算机

• CDC-ACM 的虚拟串行功能在大多数现代操作系统上可实现即插即用

• JTAG 接口可使用紧凑的 JTAG 指令实现与 CPU 调试内核的快速通信

• CDC-ACM 支持主机控制芯片复位和进入下载模式

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 USB 串口/JTAG 控制器。

管脚分配

使用内部集成 PHY 时，USB 串口/JTAG 控制器的差分信号管脚 USB_D- 和 USB_D+ 通过 IO MUX 与 GPIO19 \~ GPIO20、RTC_GPIO19 \~ RTC_GPIO20、UART1 接口和 SAR ADC2 接口复用。

使用外接 PHY 时，USB 串口/JTAG 控制器的管脚通过 IO MUX 与 GPIO38 \~ GPIO42 和 SPI 接口复用：

• VP 信号连接到 MTMS 管脚

• VM 信号连接到 MTDI 管脚

• OEN 信号连接到 MTDO 管脚

• VPO 信号连接到 MTCK 管脚

• VMO 信号连接到 GPIO38 管脚

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.9 SD/MMC 主机控制器

ESP32-S3 集成一个 SD/MMC 主机控制器。

特性

• SD 卡 3.0 和 3.01 版本

• SDIO 3.0 版本

• CE-ATA 1.1 版本

• 多媒体卡（MMC 4.41 版本、eMMC 4.5 版本和 4.51 版本）

• 高达 80 MHz 的时钟输出

• 3 种数据总线模式：

       – 1位

       – 4 位（可支持两个 SD/SDIO/MMC 4.41 卡，以及一个以 1.8 V 电压工作的 SD 卡）

       – 8位

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 SD/MMC 主机控制器。

乐鑫信息科技 24 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

管脚分配

SD/MMC 主机的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.10 LED PWM 控制器

LED PWM 控制器可以用于生成八路独立的数字波形。

特性

• 波形的周期和占空比可配置，在信号周期为 1 ms 时，占空比精确度可达 14 位

• 多种时钟源选择，包括：APB 总线时钟、外置主晶振时钟

• 可在 Light-sleep 模式下工作

• 支持硬件自动步进式地增加或减少占空比，可用于 LED RGB 彩色梯度发生器

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 LED PWM 控制器。

管脚分配

LED PWM 的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.11 电机控制脉宽调制器 (MCPWM)

ESP32-S3 包含两个 MCPWM，可以用于驱动数字马达和智能灯。每个 MCPWM 外设都包含一个时钟分频器 （预分频器） 、三个 PWM 定时器、三个 PWM 操作器和一个捕捉模块。PWM 定时器用于生成定时参考。PWM 操 作器将根据定时参考生成所需的波形。通过配置，任一 PWM 操作器可以使用任一 PWM 定时器的定时参考。不 同的 PWM 操作器可以使用相同的 PWM 定时器的定时参考来产生 PWM 信号。此外，不同的 PWM 操作器也可 以使用不同的 PWM 定时器的值来生成单独的 PWM 信号。不同的 PWM 定时器也可进行同步。

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 电机控制脉宽调制器。

管脚分配

MCPWM 的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.12 红外遥控 (RMT)

红外遥控 (RMT) 支持红外控制信号的发射和接收。

特性

• 四个通道支持发送

乐鑫信息科技 25 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

• 四个通道支持接收

• 可编程配置多个通道同时发送

• RMT 的八个通道共享 384 x 32-bit 的 RAM

• 发送脉冲支持载波调制

• 接收脉冲支持滤波和载波解调

• 乒乓发送模式

• 乒乓接收模式

• 发射器支持持续发送

• 发送通道 3 支持 DMA 访问

• 接收通道 7 支持 DMA 访问

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 红外遥控。

管脚分配

RMT 的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.1.13 脉冲计数控制器 (PCNT)

脉冲计数器 (PCNT) 通过多种模式捕捉脉冲并对脉冲边沿计数。

特性

• 四个脉冲计数控制器（单元），各自独立工作，计数范围是 1 \~ 65535

• 每个单元有两个独立的通道，共用一个脉冲计数控制器

• 所有通道均有输入脉冲信号（如 sig_ch0_un）和相应的控制信号（如 ctrl_ch0_un）

• 滤波器独立工作，过滤每个单元输入脉冲信号（sig_ch0_un 和 sig_ch1_un）控制信号（ctrl_ch0_un 和 ctrl_ch1_un）的毛刺

• 每个通道参数如下：

       1. 选择在输入脉冲信号的上升沿或下降沿计数

      2. 在控制信号为高电平或低电平时可将计数模式配置为递增、递减或停止计数

详细信息请参考 《ESP32-S3 技术参考手册》 \> 章节 脉冲计数控制器。

管脚分配

脉冲计数控制器的管脚可以为任意 GPIO，通过 GPIO 交换矩阵配置。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

乐鑫信息科技 26 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 5 外设

5.2.2 模拟信号处理 本小节描述芯片上感知和处理现实世界数据的组件。

5.2.2.1 SAR ADC

ESP32-S3 集成了两个 12 位 SAR ADC，共支持 20 个模拟通道输入。为了实现更低功耗，ESP32-S3 的 ULP 协 处理器也可以在睡眠方式下测量电压，此时，可通过设置阈值或其他触发方式唤醒 CPU。

更多信息，请参考 《ESP32-S3 技术参考手册》 \> 章节 片上传感器与模拟信号处理。

管脚分配

SAR ADC 管脚通过 IO MUX 与 GPIO1 \~ GPIO20、RTC_GPIO1 \~ RTC_GPIO20、触摸传感器接口、UART 接口、 SPI 接口、以及 USB_D- 和 USB_D+ 管脚复用。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

5.2.2.2 温度传感器

温度传感器生成一个随温度变化的电压。内部 ADC 将传感器电压转化为一个数字量。

温度传感器的测量范围为--40 °C 到 125 °C。温度传感器适用于监测芯片内部温度的变化，该温度值会随着微控 制器时钟频率或 IO 负载的变化而变化。一般来讲，芯片内部温度会高于外部温度。

更多信息，请参考 《ESP32-S3 技术参考手册》 \> 章节 片上传感器与模拟信号处理。

5.2.2.3 触摸传感器

ESP32-S3 提供了多达 14 个电容式传感 GPIO，能够探测由手指或其他物品直接接触或接近而产生的电容差异。 这种设计具有低噪声和高灵敏度的特点，可以用于支持使用相对较小的触摸板。设计中也可以使用触摸板阵列 以探测更大区域或更多点。ESP32-S3 的触摸传感器同时还支持防水和数字滤波等功能来进一步提高传感器的 性能。

说明： ESP32-S3 触摸传感器目前尚无法通过射频抗扰度测试系统 (CS) 认证，应用场景有所限制。

更多信息，请参考 《ESP32-S3 技术参考手册》 \> 章节 片上传感器与模拟信号处理。

管脚分配

触摸传感器管脚通过 IO MUX 与 GPIO1 \~ GPIO14、RTC_GPIO1 \~ RTC_GPIO14、SAR ADC 接口和 SPI 接口复 用。

更多关于管脚分配的信息，请参考 《ESP32-S3 系列芯片技术规格书》 \> 章节 IO 管脚 和 《ESP32-S3 技术参考手册》 \> 章节 IO MUX 和 GPIO 交换矩阵。

乐鑫信息科技 27 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 6 电气特性

6 电气特性

6.1 绝对最大额定值 超出表 6-1 绝对最大额定值 可能导致器件永久性损坏。这只是强调的额定值，不涉及器件在这些或其它条件下 超出表 6-2 建议工作条件 技术规格指标的功能性操作。长时间暴露在绝对最大额定条件下可能会影响模组的可 靠性。

                                            表 6-1. 绝对最大额定值

                              符号          参数                最小值         最大值           单位
                              VDD33       电源管脚电压               –0.3         3.6       V
                              TST ORE     存储温度                 –40         105        °C

6.2 建议工作条件

                                             表 6-2. 建议工作条件

                      符号       参数                       最小值            典型值        最大值          单位
                      VDD33    电源管脚电压                       3.0           3.3         3.6          V
                      IV DD    外部电源的供电电流                    0.5            —              —        A
                                            65 °C 版                                    65
                      TA       环境温度         85 °C 版         –40            —           85          °C
                                            105 °C 版                                  105

6.3 直流电气特性 (3.3 V, 25 °C)

                                        表 6-3. 直流电气特性 (3.3 V, 25 °C)

    参数          说明                                                     最小值            典型值                 最大值          单位
    CIN         管脚电容                                                        —                 2                 —      pF
    VIH         高电平输入电压                                           0.75 × VDD 1                —             1
                                                                                                         VDD + 0.3     V
    VIL         低电平输入电压                                                     –0.3              —         0.25 × VDD 1   V
    IIH         高电平输入电流                                                           —           —                  50    nA
    IIL         低电平输入电流                                                        —              —                  50    nA
    VOH    2    高电平输出电压                                               0.8 × VDD 1             —                   —    V
    VOL    2    低电平输出电压                                                           —           —          0.1 × VDD 1   V
                高电平拉电流 (VDD 1 = 3.3 V, V       OH >= 2.64 V,
    IOH                                                                           —           40                  —    mA
                PAD_DRIVER = 3)
                低电平灌电流 (VDD 1 = 3.3 V, VOL = 0.495 V,
    IOL                                                                           —           28                  —    mA
                PAD_DRIVER = 3)
    RP U        内部弱上拉电阻                                                           —           45                  —    kΩ
    RP D        内部弱下拉电阻                          —                                            45                —      kΩ
    VIH_nRST    芯片复位释放电压（EN 管脚应满足电压范围） 0.75 × VDD 1                                           —             1
                                                                                                         VDD + 0.3     V
    VIL_nRST    芯片复位电压（EN 管脚应满足电压范围）                                        –0.3              —         0.25 × VDD 1   V

乐鑫信息科技 28 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 6 电气特性

    1 VDD – 各个电源域电源管脚的电压。
    2V
      OH 和 VOL 为负载是高阻条件下的测试值。

6.4 功耗特性 6.4.1 Active 模式下的功耗 因使用了先进的电源管理技术，模组可以在不同的功耗模式之间切换。关于不同功耗模式的描述，详见 《ESP32-S3 系列芯片技术规格书》 的 电源管理单元章节。

下列功耗数据是基于 3.3 V 供电电源、25 °C 环境温度的条件下测得。

所有发射功耗数据均基于 100% 占空比测得。

所有接收功耗数据均是在外设关闭、CPU 空闲的条件下测得。

                          表 6-4. Active 模式下 Wi-Fi (2.4 GHz) 功耗特性

         工作模式            射频模式          描述                                      峰值 (mA)
                                       802.11b, 1 Mbps, @20.5 dBm                     355
                                       802.11g, 54 Mbps, @18 dBm                       297
                         发射 (TX)
                                       802.11n, HT20, MCS7, @17.5 dBm                 286
         Active（射频工作）
                                       802.11n, HT40, MCS7, @17 dBm                   285
                                       802.11b/g/n, HT20                                95
                         接收 (RX)
                                       802.11n, HT40                                    97


                            表 6-5. Active 模式下低功耗蓝牙功耗特性

         工作模式            射频模式          描述                                      峰值 (mA)
                                       低功耗蓝牙 @ 20.0 dBm                               344
                         发射 (TX)       低功耗蓝牙 @ 9.0 dBm                                202
         Active (射频工作)                 低功耗蓝牙 @ 0 dBm                                   187
                                       低功耗蓝牙 @ –15.0 dBm                               119
                         接收 (RX)       低功耗蓝牙                                            93



    说明：
    以下内容摘自 《ESP32-S3 系列芯片技术规格书》 的 其他功耗模式下的功耗章节。

6.4.2 其他功耗模式下的功耗 请注意，若模组内置芯片封装内有 PSRAM，功耗数据可能略高于下表数据。

乐鑫信息科技 29 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 6 电气特性

                                      表 6-6. Modem-sleep 模式下的功耗

                       频率                                                        典型值1       典型值2
    工作模式              (MHz)        说明                                             (mA)        (mA)
                                   WAITI（双核均空闲）                                      13.2        18.8
                                   单核执行 32 位数据访问指令，另一个核空闲                            16.2        21.8
                                   双核执行 32 位数据访问指令                                   18.7       24.4
                              40   单核执行 128 位数据访问指令，另一个核空闲                           19.9       25.4
                                   双核执行 128 位数据访问指令                                  23.0       28.8
                                   WAITI                                             22.0        36.1
                                   单核执行 32 位数据访问指令，另一个核空闲                            28.4       42.6
                                   双核执行 32 位数据访问指令                                   33.1        47.3
                              80   单核执行 128 位数据访问指令，另一个核空闲                           35.1        49.6
                                   双核执行 128 位数据访问指令                                  41.8       56.3
                                   WAITI                                             27.6       42.3
                                   单核执行 32 位数据访问指令，另一个核空闲                            39.9       54.6
                                   双核执行 32 位数据访问指令                                   49.6        64.1
                             160   单核执行 128 位数据访问指令，另一个核空闲                           54.4       69.2
    Modem-sleep3
                                   双核执行 128 位数据访问指令                                  66.7         81.1
                                   WAITI                                             32.9        47.6
                                   单核执行 32 位数据访问指令，另一个核空闲                            51.2       65.9
                                   双核执行 32 位数据访问指令                                   66.2        81.3
                             240   单核执行 128 位数据访问指令，另一个核空闲                           72.4        87.9
                                   双核执行 128 位数据访问指令                                  91.7       107.9
    1 所有外设时钟关闭时的典型值。
    2 所有外设时钟打开时的典型值。实际情况下，外设在不同工作状态下电流会有所差异。
    3 Modem-sleep 模式下，Wi-Fi 设有时钟门控。该模式下，访问 flash 时功耗会增加。若 flash 速率为 80 Mbit/s，
     SPI 双线模式下 flash 的功耗为 10 mA。


                                           表 6-7. 低功耗模式下的功耗

              工作模式            说明                                           典型值 (µA)
              Light-sleep1    VDD_SPI 和 Wi-Fi 掉电，所有 GPIO 设置为高阻状态                   240
                              RTC 存储器和 RTC 外设上电                                      8
              Deep-sleep
                              RTC 存储器上电，RTC 外设掉电                                     7
              关闭              EN 管脚拉低，芯片关闭                                           1
              1 Light-sleep 模式下，SPI 相关管脚上拉。封装内有 PSRAM 的芯片请在典型值的基
               础上添加相应的 PSRAM 功耗：8 MB Octal PSRAM (3.3 V) 为 140 µA；8 MB Octal
               PSRAM (1.8 V) 为 200 µA；2 MB Quad PSRAM 为 40 µA。

6.5 存储器规格 本节数据来源于存储器供应商的数据手册。以下数值已在设计阶段和/或特性验证中得到确认，但未在生产中进 行全面测试。设备出厂时，存储器均为擦除状态。

乐鑫信息科技 30 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 6 电气特性

                                      表 6-8. Flash 规格

           参数          说明                     最小值           典型值           最大值           单位
                       电源电压 (1.8 V)                 1.65          1.80          2.00     V
           VCC
                       电源电压 (3.3 V)                 2.7           3.3            3.6     V
           FC          最大时钟频率                        80             —             —     MHz
           —           编程/擦除周期               100,000                —             —     次
           TRET        数据保留时间                        20             —             —     年
           TP P        页编程时间                          —           0.8             5     ms
           TSE         扇区擦除时间 (4 KB)                  —            70           500     ms
           TBE1        块擦除时间 (32 KB)                  —           0.2             2      s
           TBE2        块擦除时间 (64 KB)                  —           0.3             3      s
                       芯片擦除时间 (16 Mb)                 —             7            20      s
                       芯片擦除时间 (32 Mb)                 —            20            60      s
           TCE         芯片擦除时间 (64 Mb)                 —            25           100      s
                       芯片擦除时间 (128 Mb)                —            60           200      s
                       芯片擦除时间 (256 Mb)                —            70           300      s


                                      表 6-9. PSRAM 规格

                  参数     说明                最小值       典型值            最大值           单位
                         电源电压 (1.8 V)        1.62          1.80          1.98      V
                  VCC
                         电源电压 (3.3 V)        2.7           3.3           3.6       V
                  FC     最大时钟频率               80             —            —       MHz

乐鑫信息科技 31 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 7 射频特性

7 射频特性 本章提供产品的射频特性表。

射频数据是在天线端口处连接射频线后测试所得，包含了射频前端电路带来的损耗。带有外部天线连接器的受 测模组所使用的外部天线具有 50 Ω 阻抗。 工作信道中心频率范围应符合国家或地区的规范标准。软件可以配置工作信道中心频率范围，具体请参 考《ESP 射频测试指南》。

除非特别说明，射频测试均是在 3.3 V (±5%) 供电电源、25 °C 环境温度的条件下完成。

7.1 Wi-Fi 射频

                                      表 7-1. Wi-Fi 射频规格

               名称                                 描述
               工作信道中心频率范围                         2412 ~ 2484 MHz
               无线标准                               IEEE 802.11b/g/n

7.1.1 Wi-Fi 射频发射器 (TX) 特性

                     表 7-2. 频谱模板和 EVM 符合 802.11 标准时的发射功率

                                                        最小值       典型值       最大值
               速率
                                                        (dBm)      (dBm)     (dBm)
               802.11b, 1 Mbps                                —      20.5           —
               802.11b, 11 Mbps                               —      20.5           —
               802.11g, 6 Mbps                                —      20.0           —
               802.11g, 54 Mbps                               —      18.0           —
               802.11n, HT20, MCS 0                           —      19.0           —
               802.11n, HT20, MCS 7                           —      17.5           —
               802.11n, HT40, MCS 0                           —      18.5           —
               802.11n, HT40, MCS 7                           —      17.0           —


                                      表 7-3. 发射 EVM 测试1

                                                      最小值         典型值       标准限值
             速率
                                                       (dB)       (dB)       (dB)
             802.11b, 1 Mbps, @20.5 dBm                   —       –24.5         –10
             802.11b, 11 Mbps, @20.5 dBm                  —       –24.5         –10
             802.11g, 6 Mbps, @20 dBm                     —       –23.0         –5
             802.11g, 54 Mbps, @18 dBm                    —       –29.5        –25
             802.11n, HT20, MCS 0, @19 dBm                —       –24.0         –5
             802.11n, HT20, MCS 7, @17.5 dBm              —       –30.5        –27
             802.11n, HT40, MCS 0, @18.5 dBm              —       –25.0         –5
                                                                             见下页

乐鑫信息科技 32 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 7 射频特性

                                     表 7-3 – 接上页
                                                  最小值        典型值       标准限值
             速率
                                                  (dB)       (dB)       (dB)
             802.11n, HT40, MCS 7, @17 dBm           —       –30.0        –27
              1 发射 EVM 的每个测试项对应的发射功率为表 7-2 频谱模板和 EVM 符
               合 802.11 标准时的发射功率 中提供的典型值。

7.1.2 Wi-Fi 射频接收器 (RX) 特性 802.11b 标准下的误包率 (PER) 不超过 8%，802.11g/n 标准下不超过 10%。

                                    表 7-4. 接收灵敏度

                                                  最小值        典型值       最大值
             速率
                                                   (dBm)      (dBm)     (dBm)
             802.11b, 1 Mbps                             —    –98.2            —
             802.11b, 2 Mbps                             —    –95.6            —
             802.11b, 5.5 Mbps                           —    –92.8            —
             802.11b, 11 Mbps                            —     –88.5           —
             802.11g, 6 Mbps                             —    –93.0            —
             802.11g, 9 Mbps                             —    –92.0            —
             802.11g, 12 Mbps                            —    –90.8            —
             802.11g, 18 Mbps                            —     –88.5           —
             802.11g, 24 Mbps                            —    –85.5            —
             802.11g, 36 Mbps                            —    –82.2            —
             802.11g, 48 Mbps                            —     –78.0           —
             802.11g, 54 Mbps                            —     –76.2           —
             802.11n, HT20, MCS 0                        —    –93.0            —
             802.11n, HT20, MCS 1                        —    –90.6            —
             802.11n, HT20, MCS 2                        —     –88.4           —
             802.11n, HT20, MCS 3                        —     –84.8           —
             802.11n, HT20, MCS 4                        —     –81.6           —
             802.11n, HT20, MCS 5                        —     –77.4           —
             802.11n, HT20, MCS 6                        —     –75.6           —
             802.11n, HT20, MCS 7                        —     –74.2           —
             802.11n, HT40, MCS 0                        —    –90.0            —
             802.11n, HT40, MCS 1                        —     –87.5           —
             802.11n, HT40, MCS 2                        —    –85.0            —
             802.11n, HT40, MCS 3                        —    –82.0            —
             802.11n, HT40, MCS 4                        —     –78.5           —
             802.11n, HT40, MCS 5                        —     –74.4           —
             802.11n, HT40, MCS 6                        —     –72.5           —
             802.11n, HT40, MCS 7                        —     –71.2           —

乐鑫信息科技 33 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 7 射频特性

                                      表 7-5. 最大接收电平

                                                        最小值        典型值        最大值
             速率
                                                        (dBm)      (dBm)      (dBm)
             802.11b, 1 Mbps                                —           5        —
             802.11b, 11 Mbps                               —           5        —
             802.11g, 6 Mbps                                —           5        —
             802.11g, 54 Mbps                               —           0        —
             802.11n, HT20, MCS 0                           —           5        —
             802.11n, HT20, MCS 7                           —           0        —
             802.11n, HT40, MCS 0                           —           5        —
             802.11n, HT40, MCS 7                           —           0        —


                                      表 7-6. 接收邻道抑制

                                                        最小值        典型值        最大值
             速率
                                                         (dB)       (dB)      (dB)
             802.11b, 1 Mbps                                —          35        —
             802.11b, 11 Mbps                               —          35        —
             802.11g, 6 Mbps                                —          31        —
             802.11g, 54 Mbps                               —          14        —
             802.11n, HT20, MCS 0                           —          31        —
             802.11n, HT20, MCS 7                           —          13        —
             802.11n, HT40, MCS 0                           —          19        —
             802.11n, HT40, MCS 7                           —           8        —

7.2 低功耗蓝牙射频 表 7-7. 低功耗蓝牙射频规格

             名称                                    描述
             工作信道中心频率范围                            2402 ~ 2480 MHz
             射频发射功率范围                              –24.0 ~ 20.0 dBm

7.2.1 低功耗蓝牙射频发射器 (TX) 特性

                          表 7-8. 低功耗蓝牙 - 发射器特性 - 1 Mbps

      参数                描述                              最小值        典型值         最大值        单位
                        |fn |n=0, 1, 2, ..k 最大值             —         2.50            —   kHz
                        |f0 − fn | 最大值                      —         2.00            —   kHz
      载波频率偏移和漂移
                        |fn − fn−5 | 最大值                    —          1.40           —   kHz
                        |f1 − f0 |                          —          1.00           —   kHz
                        ∆ f 1avg                            —       249.00            —   kHz
                        ∆ f 2max 最小值
      调制特性                                                  —       198.00            —   kHz
                      （至少 99.9% 的 ∆ f 2max ）
                                                                                          见下页

乐鑫信息科技 34 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 7 射频特性

                                   表 7-8 – 接上页
      参数           描述                            最小值      典型值        最大值       单位
                   ∆ f 2avg /∆ f 1avg              —         0.86         —     —
                   ± 2 MHz 偏移                      —       –37.00         —    dBm
      带内杂散发射       ± 3 MHz 偏移                      —       –42.00         —    dBm
                   > ± 3 MHz 偏移                    —       –44.00         —    dBm


                    表 7-9. 低功耗蓝牙 - 发射器特性 - 2 Mbps

      参数           描述                            最小值      典型值        最大值       单位
                   |fn |n=0, 1, 2, ..k 最大值         —         2.50         —     kHz
                   |f0 − fn | 最大值                  —         2.00         —     kHz
      载波频率偏移和漂移
                   |fn − fn−5 | 最大值                —          1.40        —     kHz
                   |f1 − f0 |                      —          1.00        —     kHz
                   ∆ f 1avg                        —       499.00         —     kHz
                   ∆ f 2max 最小值
      调制特性                                         —       416.00         —     kHz
                  （至少 99.9% 的 ∆ f 2max ）
                   ∆ f 2avg /∆ f 1avg              —         0.89         —     —
                   ± 4 MHz 偏移                      —       –42.00         —    dBm
      带内杂散发射       ± 5 MHz 偏移                      —       –44.00         —    dBm
                   > ± 5 MHz 偏移                    —       –47.00         —    dBm


                   表 7-10. 低功耗蓝牙 - 发射器特性 - 125 Kbps

      参数           描述                            最小值      典型值        最大值       单位
                   |fn |n=0, 1, 2, ..k 最大值         —         0.80         —     kHz
                   |f0 − fn | 最大值                  —          1.00        —     kHz
      载波频率偏移和漂移
                   |fn − fn−3 |                    —         0.30         —     kHz
                   |f0 − f3 |                      —          1.00        —     kHz
                   ∆ f 1avg                        —       248.00         —     kHz
      调制特性         ∆ f 1max 最小值
                                                   —       222.00         —     kHz
                  （至少 99.9% 的 ∆ f 1max ）
                   ± 2 MHz 偏移                      —       –37.00         —    dBm
      带内杂散发射       ± 3 MHz 偏移                      —       –42.00         —    dBm
                   > ± 3 MHz 偏移                    —       –44.00         —    dBm


                   表 7-11. 低功耗蓝牙 - 发射器特性 - 500 Kbps

      参数           描述                            最小值      典型值        最大值       单位
                   |fn |n=0, 1, 2, ..k 最大值         —         0.80         —     kHz
                   |f0 − fn | 最大值                  —          1.00        —     kHz
      载波频率偏移和漂移
                   |fn − fn−3 |                    —         0.85         —     kHz
                   |f0 − f3 |                      —         0.34         —     kHz
                   ∆ f 2avg                        —       213.00         —     kHz
      调制特性         ∆ f 2max 最小值
                                                   —       196.00         —     kHz
                  （至少 99.9% 的 ∆ f 2max ）
                                                                              见下页

乐鑫信息科技 35 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 7 射频特性

                                     表 7-11 – 接上页
         参数             描述                          最小值      典型值        最大值        单位
                        ± 2 MHz 偏移                    —       –37.00           —   dBm
         带内杂散发射         ± 3 MHz 偏移                    —       –42.00           —   dBm
                        > ± 3 MHz 偏移                  —       –44.00           —   dBm

7.2.2 低功耗蓝牙射频接收器 (RX) 特性

                        表 7-12. 低功耗蓝牙 - 接收器特性 - 1 Mbps

    参数                         描述                          最小值      典型值        最大值       单位
    灵敏度 @30.8% PER             —                               —       –96.5       —     dBm
    最大接收信号 @30.8% PER          —                               —          8        —     dBm
    共信道抑制比 C/I                 F = F0 MHz                      —          8        —     dB
                               F = F0 + 1 MHz                  —          4        —     dB
                               F = F0 – 1 MHz                  —          4        —     dB
                               F = F0 + 2 MHz                  —        –23        —     dB
                               F = F0 – 2 MHz                  —        –23        —     dB
    邻道选择性抑制比 C/I
                               F = F0 + 3 MHz                  —        –34        —     dB
                               F = F0 – 3 MHz                  —        –34        —     dB
                               F > F0 + 3 MHz                  —        –36        —     dB
                               F > F0 – 3 MHz                  —        –37        —     dB
    镜像频率                       —                               —        –36        —     dB
                               F = Fimage + 1 MHz              —        –39        —     dB
    邻道镜像频率干扰
                               F = Fimage – 1 MHz              —        –34        —     dB
                               30 MHz ~ 2000 MHz               —         –12       —     dBm
                               2003 MHz ~ 2399 MHz             —         –18       —     dBm
    带外阻塞
                               2484 MHz ~ 2997 MHz             —         –16       —     dBm
                               3000 MHz ~ 12.75 GHz            —         –10       —     dBm
    互调                         —                               —        –29        —     dBm



                        表 7-13. 低功耗蓝牙 - 接收器特性 - 2 Mbps

    参数                         描述                          最小值      典型值        最大值       单位
    灵敏度 @30.8% PER             —                               —        –92        —     dBm
    最大接收信号 @30.8% PER          —                               —          3        —     dBm
    共信道干扰 C/I                  F = F0 MHz                      —          8        —     dB
                               F = F0 + 2 MHz                  —          4        —     dB
                               F = F0 – 2 MHz                  —          4        —     dB
                               F = F0 + 4 MHz                  —        –27        —     dB
                               F = F0 – 4 MHz                  —        –27        —     dB
    邻道选择性抑制比 C/I
                               F = F0 + 6 MHz                  —        –38        —     dB
                               F = F0 – 6 MHz                  —        –38        —     dB
                               F > F0 + 6 MHz                  —         –41       —     dB
                                                                                       见下页

乐鑫信息科技 36 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 7 射频特性

                                   表 7-13 – 接上页
    参数                        描述                      最小值      典型值       最大值      单位
                              F > F0 – 6 MHz              —        –41       —     dB
    镜像频率                      —                           —        –27       —     dB
                              F = Fimage + 2 MHz          —        –38       —     dB
    邻道镜像频率干扰
                              F = Fimage – 2 MHz          —          4       —     dB
                              30 MHz ~ 2000 MHz           —        –15       —    dBm
                              2003 MHz ~ 2399 MHz         —        –21       —    dBm
    带外阻塞
                              2484 MHz ~ 2997 MHz         —        –21       —    dBm
                              3000 MHz ~ 12.75 GHz        —         –9       —    dBm
    互调                        —                           —        –29       —    dBm



                        表 7-14. 低功耗蓝牙 - 接收器特性 - 125 Kbps

    参数                        描述                      最小值      典型值       最大值      单位
    灵敏度 @30.8% PER            —                           —     –103.5       —    dBm
    最大接收信号 @30.8% PER         —                           —          8       —    dBm
    共信道抑制比 C/I                F = F0 MHz                  —          4       —     dB
                              F = F0 + 1 MHz              —          1       —     dB
                              F = F0 – 1 MHz              —          2       —     dB
                              F = F0 + 2 MHz              —        –26       —     dB
                              F = F0 – 2 MHz              —        –26       —     dB
    邻道选择性抑制比 C/I
                              F = F0 + 3 MHz              —       –36        —     dB
                              F = F0 – 3 MHz              —        –39       —     dB
                              F > F0 + 3 MHz              —        –42       —     dB
                              F > F0 – 3 MHz              —        –43       —     dB
    镜像频率                      —                           —        –42       —     dB
                              F = Fimage + 1 MHz          —        –43       —     dB
    邻道镜像频率干扰
                              F = Fimage – 1 MHz          —       –36        —     dB


                        表 7-15. 低功耗蓝牙 - 接收器特性 - 500 Kbps

    参数                        描述                      最小值      典型值       最大值      单位
    灵敏度 @30.8% PER            —                           —       –100       —    dBm
    最大接收信号 @30.8% PER         —                           —          8       —    dBm
    共信道抑制比 C/I                F = F0 MHz                  —          4       —     dB
                              F = F0 + 1 MHz              —          1       —     dB
                              F = F0 – 1 MHz              —          0       —     dB
                              F = F0 + 2 MHz              —        –24       —     dB
                              F = F0 – 2 MHz              —        –24       —     dB
    邻道选择性抑制比 C/I
                              F = F0 + 3 MHz              —        –37       —     dB
                              F = F0 – 3 MHz              —        –39       —     dB
                              F > F0 + 3 MHz              —        –38       —     dB
                              F > F0 – 3 MHz              —        –42       —     dB
                                                                                 见下页

乐鑫信息科技 37 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 7 射频特性

                    表 7-15 – 接上页
    参数         描述                    最小值      典型值       最大值      单位
    镜像频率       —                         —        –38       —     dB
               F = Fimage + 1 MHz        —        –42       —     dB
    邻道镜像频率干扰
               F = Fimage – 1 MHz        —        –37       —     dB

乐鑫信息科技 38 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见  乐鑫信息科技

                                                                                                                                                                                                                                                                                                                                      8 模组原理图
                                                  8 模组原理图
                                                  模组内部元件的电路图。在内置 PSRAM 的模组中，芯片已通过 eFuse 设置将 VDD_SPI 电压固定为 3.3 V 或 1.8 V，因此这些模组的 VDD_SPI 电压不受 GPIO45 电平
                                                  影响；但在使用其他模组时，请确保模组上电时外部电路不会将 GPIO45 拉高。
                                                                             5                                                    4                                                        3                                               2                                                        1



                                                                                                                                                          GND


                                                                                                                                                    GND                          GND
                                                                                                                                                                 Y1




                                                                                                                                                          4



                                                                                                                                                                      3
                                                                                                                                                           GND



                                                                                                                                                                      GND XOUT
                                                                                                     The values of C1 and C4 vary with              C1                            C4
                                                       D                                                                                                                                                                                                                                                                          D
                                                                                                     the selection of the crystal.                 TBD                            TBD                  VDD33                       VDD33        VDD33 GND                                                                GND




                                                                                                                                                           XIN
                                                                                                                                                                                                                                                                     U3           ESP32-S3-WROOM-1
                                                                                                     The value of R4 varies with the                                                                                                                                                                        41
                                                                                                                                                                                                                                                                                                  EPAD




                                                                                                                                                          1



                                                                                                                                                                      2
                                                                                                     actual PCB board. R4 could be a                                                                                                                           1
                                                                                                                                                                                                                                                                     GND                           GND
                                                                                                                                                                                                                                                                                                            40
                                                                                                                                                                                                          R1                                                   2                                            39        GPIO1
                                                                                                     resistor or inductor, the initial                                                                                                 D1         CHIP_PU      3     3V3                            IO1     38        GPIO2
                                                                                                     value is suggested to be 24 nH.                               GND                                    10K(NC)                      ESD        GPIO4        4     EN                             IO2     37        U0TXD
                                                           VDD33                                                                                          40MHz(±10ppm)                                                                           GPIO5        5     IO4                          TXD0      36        U0RXD
                                                                                                                                                                                                                        GPIO46                    GPIO6        6     IO5                          RXD0      35        GPIO42
                                                                                                                                                                                                                        GPIO45                    GPIO7        7     IO6                           IO42     34        GPIO41
                                                                                                                                                                                                                        U0RXD                     GPIO15       8     IO7                           IO41     33        GPIO40
                                                                                       C3                  C2                                                                                            R3         499 U0TXD      GND            GPIO16       9     IO15                          IO40     32        GPIO39
                                                                                                                                                                                                                        GPIO42                    GPIO17      10     IO16                          IO39     31        GPIO38
                                                                                       1uF                10nF                                                                                                          GPIO41                    GPIO18      11     IO17                          IO38     30        GPIO37




                                                                                                                                                    0
                                                                                                                                                                                                                        GPIO40                    GPIO8       12     IO18                          IO37     29        GPIO36
                                                           VDD33                                                                                                                                                        GPIO39                    GPIO19      13     IO8                           IO36     28        GPIO35

反馈文档意见

                                                                                        GND                 GND                            GND                                                                          GPIO38                    GPIO20      14     IO19                          IO35     27        GPIO0
                                                                                           L1             2.0nH(0.1nH)                                                                                                                                               IO20                           IO0




                                                                                                                                                    R4




                                                                                                                                                                                                                                                                      IO46

                                                                                                                                                                                                                                                                      IO10
                                                                                                                                                                                                                                                                      IO11
                                                                                                                                                                                                                                                                      IO12
                                                                                                                                                                                                                                                                      IO13
                                                                                                                                                                                                                                                                      IO14
                                                                                                                                                                                                                                                                      IO21
                                                                                                                                                                                                                                                                      IO47
                                                                                                                                                                                                                                                                      IO48
                                                                                                                                                                                                                                                                      IO45
                                                             C6                  C7          C8            C9                                                                                            C10




                                                                                                                                                                                                                                                                      IO3

                                                                                                                                                                                                                                                                      IO9
                                                       C                                                                                                                                                                                                                                                                          C
         39




                                                                                                                                                                                                                          VDD33


                                                                                                                                           57


                                                                                                                                                  56
                                                                                                                                                  55
                                                                                                                                                  54
                                                                                                                                                  53
                                                                                                                                                  52
                                                                                                                                                  51
                                                                                                                                                  50
                                                                                                                                                  49
                                                                                                                                                  48
                                                                                                                                                  47
                                                                                                                                                  46
                                                                                                                                                  45
                                                                                                                                                  44
                                                                                                                                                  43
                                                             10uF                1uF         0.1uF       0.1uF                                                                                           0.1uF




                                                                                                                                                                                                                                                                     15
                                                                                                                                                                                                                                                                     16
                                                                                                                                                                                                                                                                     17
                                                                                                                                                                                                                                                                     18
                                                                                                                                                                                                                                                                     19
                                                                                                                                                                                                                                                                     20
                                                                                                                                                                                                                                                                     21
                                                                                                                                                                                                                                                                     22
                                                                                                                                                                                                                                                                     23
                                                                                                                                                                                                                                                                     24
                                                                                                                                                                                                                                                                     25
                                                                                                                                                                                                                                                                     26
                                                                                                                                                        VDDA
                                                                                                                                                        VDDA
                                                                                                                                            GND




                                                                                                                                                       U0RXD
                                                                                                                                                       U0TXD
                                                                                                                                                        MTMS


                                                                                                                                                        MTDO
                                                                                                                                                        MTCK
                                                                                                                                                      XTAL_P
                                                                                                                                                      XTAL_N
                                                                                                                                                      GPIO46
                                                                                                                                                      GPIO45



                                                                                                                                                         MTDI
                                                                                                                                                  VDD3P3_CPU


                                                                                                                                                      GPIO38
                                                           GND               GND        GND                 GND                                                                                        GND




                                                                                                                                                                                                                                                                     GPIO46

                                                                                                                                                                                                                                                                     GPIO10
                                                                                                                                                                                                                                                                     GPIO11
                                                                                                                                                                                                                                                                     GPIO12
                                                                                                                                                                                                                                                                     GPIO13
                                                                                                                                                                                                                                                                     GPIO14
                                                                                                                                                                                                                                                                     GPIO21
                                                                                                                                                                                                                                                                     GPIO47
                                                                                                                                                                                                                                                                     GPIO48
                                                                                                                                                                                                                                                                     GPIO45
                                                                                                                                                                                                                                                                     GPIO3

                                                                                                                                                                                                                                                                     GPIO9
                                                           ANT1        50 ohm Impedance Control
                                                                   1   RF_ANT                 L2          TBD      LNA_IN     1                                                                   42                      GPIO37
                                                                   2                                                          2       LNA_IN                                             GPIO37   41                      GPIO36
                                                                                                                                      VDD3P3                                             GPIO36
                                                                                 L3    C11                C12
                                                                                                                   CHIP_PU
                                                                                                                              3
                                                                                                                                      VDD3P3                                             GPIO35
                                                                                                                                                                                                  40                      GPIO35                               ESP32-S3-WROOM-1(pin-out)
                                                           PCB_ANT                                                            4                                                                   39
                                                                                 TBD   TBD                TBD      GPIO0      5       CHIP_PU                                            GPIO34   38
         ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7




                                                                                                                   GPIO1      6       GPIO0                                              GPIO33   37                      GPIO47
                                                                                                                   GPIO2      7       GPIO1                                            SPICLK_P   36                      GPIO48                                                  VDD_SPI
                                                                       GND              GND                 GND    GPIO3      8       GPIO2                                            SPICLK_N   35   R16        0       SPID
                                                                                 C5                                                   GPIO3                                                SPID
                                                                                                                   GPIO4      9                                                                   34   R15        0       SPIQ
                                                                                                                                      GPIO4                                                SPIQ




                                                                                                                                                                                                                                                                                    8
                                                                                 TBD                               GPIO5     10                                                                   33   R10        0       SPICLK
                                                                                                                   GPIO6     11       GPIO5                                              SPICLK   32                      SPICS0
                                                                                                                                      GPIO6                                              SPICS0




                                                                                                                                                                                                                                                                                    VDD
                                                                                                                   GPIO7     12                                                                   31   R14        0       SPIWP                             SPICS0     1                             5      SPID
                                                                                                                   GPIO8     13       GPIO7                                               SPIWP   30   R13        0       SPIHD                                             /CS               DI
                                                       B                     GND                                                                                                                                                                                                                                                  B
                                                                                                                   GPIO9     14       GPIO8                                               SPIHD   29                                                        SPICLK     6                             2      SPIQ
                                                                                                                                      GPIO9                                             VDD_SPI                                                                             CLK              DO
                                                                                                                                                  VDD3P3_RTC




                                                           The values of L3, C5, C11, L2 and C12
                                                                                                                                                  XTAL_32K_N
                                                                                                                                                  XTAL_32K_P




                                                                                                                                                                                                                                                            SPIHD      7                             3      SPIWP
                                                           vary with the actual PCB board.                                                                                                                                                                                  /HOLD            /WP




                                                                                                                                                                                                                                                                                    GND
                                                                                                                                                                                                         C13        C14 VDD_SPI
                                                                                                                                                  GPIO10
                                                                                                                                                  GPIO11
                                                                                                                                                  GPIO12
                                                                                                                                                  GPIO13
                                                                                                                                                  GPIO14



                                                                                                                                                  GPIO17
                                                                                                                                                  GPIO18
                                                                                                                                                  GPIO19
                                                                                                                                                  GPIO20
                                                                                                                                                  GPIO21
                                                                                                                                                  SPICS1




                                                           NC: No component.                                                                                                                             0.1uF      1uF                                                     U2            FLASH




                                                                                                                                                                                                                                                                                    4
                                                                                                                                      U1                                           ESP32-S3
                                                                                                                                                  15
                                                                                                                                                  16
                                                                                                                                                  17
                                                                                                                                                  18
                                                                                                                                                  19
                                                                                                                                                  20
                                                                                                                                                  21
                                                                                                                                                  22
                                                                                                                                                  23
                                                                                                                                                  24
                                                                                                                                                  25
                                                                                                                                                  26
                                                                                                                                                  27
                                                                                                                                                  28




                                                                                                                  VDD33                                                            ESP32-S3R2          GND       GND                                                                GND
                                                                                                                                                                                   ESP32-S3R8
                                                                                                                                                                                   ESP32-S3R16V

                                                                                                                                       C15
                                                                                                                                                  GPIO10
                                                                                                                                                  GPIO11
                                                                                                                                                  GPIO12
                                                                                                                                                  GPIO13
                                                                                                                                                  GPIO14

                                                                                                                                                            GPIO15
                                                                                                                                                            GPIO16
                                                                                                                                                            GPIO17
                                                                                                                                                            GPIO18
                                                                                                                                                            GPIO19
                                                                                                                                                            GPIO20
                                                                                                                                                            GPIO21




                                                                                                                                      0.1uF


                                                                                                                                           GND

                                                       A                                                                                                                                                                                                                                                                          A


                                                                                                                                                         图 8-1. ESP32-S3-WROOM-1 原理图                                                   Title
                                                                                                                                                                                                                                                  <ESP32-S3-WROOM-1>

                                                                                                                                                                                                                                       Size     Page Name                                  Rev
                                                                                                                                                                                                                                           A4     <02_ESP32-S3-WROOM-1>                            Confidential and Proprietary
                                                                                                                                                                                                                                                                                            V1.4
                                                                                                                                                                                                                                       Date:        Tuesday, November 21, 2023             Sheet        2        of      2
                                                                             5                                                    4                                                        3                                               2                                                        1

5 4 3 2 1 乐鑫信息科技

                                                                                                                                                                                                                                                                                                                              8 模组原理图
                                                                                                                                                 GND


                                                                                                                                           GND                          GND
                                                                                                                                                        Y1




                                                                                                                                                 4



                                                                                                                                                             3
                                                                                                                                                  GND



                                                                                                                                                             GND XOUT
                                                                                            The values of C1 and C4 vary with              C1                            C4
                                                  D                                                                                                                                                                                                                                                                       D
                                                                                            the selection of the crystal.                 TBD                            TBD                  VDD33                       VDD33        VDD33 GND                                                                 GND




                                                                                                                                                  XIN
                                                                                                                                                                                                                                                            U3          ESP32-S3-WROOM-1U
                                                                                            The value of R4 varies with the                                                                                                                                                                         41
                                                                                                                                                                                                                                                                                          EPAD




                                                                                                                                                 1



                                                                                                                                                             2
                                                                                            actual PCB board. R4 could be a                                                                                                                           1
                                                                                                                                                                                                                                                            GND                            GND
                                                                                                                                                                                                                                                                                                    40
                                                                                                                                                                                                 R1                                                   2                                             39        GPIO1
                                                                                            resistor or inductor, the initial                                                                                                 D1         CHIP_PU      3     3V3                             IO1     38        GPIO2
                                                                                            value is suggested to be 24 nH.                               GND                                    10K(NC)                      ESD        GPIO4        4     EN                              IO2     37        U0TXD
                                                      VDD33                                                                                      40MHz(±10ppm)                                                                           GPIO5        5     IO4                           TXD0      36        U0RXD
                                                                                                                                                                                                               GPIO46                    GPIO6        6     IO5                           RXD0      35        GPIO42
                                                                                                                                                                                                               GPIO45                    GPIO7        7     IO6                            IO42     34        GPIO41
                                                                                                                                                                                                               U0RXD                     GPIO15       8     IO7                            IO41     33        GPIO40
                                                                              C3                  C2                                                                                            R3         499 U0TXD      GND            GPIO16       9     IO15                           IO40     32        GPIO39
                                                                                                                                                                                                               GPIO42                    GPIO17      10     IO16                           IO39     31        GPIO38
                                                                              1uF                10nF                                                                                                          GPIO41                    GPIO18      11     IO17                           IO38     30        GPIO37




                                                                                                                                           0
                                                                                                                                                                                                               GPIO40                    GPIO8       12     IO18                           IO37     29        GPIO36
                                                      VDD33                                                                                                                                                    GPIO39                    GPIO19      13     IO8                            IO36     28        GPIO35
                                                                                GND                GND                            GND                                                                          GPIO38                    GPIO20      14     IO19                           IO35     27        GPIO0
                                                                                   L1            2.0nH(0.1nH)                                                                                                                                               IO20                            IO0




                                                                                                                                           R4




                                                                                                                                                                                                                                                             IO46

                                                                                                                                                                                                                                                             IO10
                                                                                                                                                                                                                                                             IO11
                                                                                                                                                                                                                                                             IO12
                                                                                                                                                                                                                                                             IO13
                                                                                                                                                                                                                                                             IO14
                                                                                                                                                                                                                                                             IO21
                                                                                                                                                                                                                                                             IO47
                                                                                                                                                                                                                                                             IO48
                                                                                                                                                                                                                                                             IO45
                                                          C6            C7          C8            C9                                                                                            C10




                                                                                                                                                                                                                                                             IO3

                                                                                                                                                                                                                                                             IO9
                                                  C                                                                                                                                                                                                                                                                       C
                                                                                                                                                                                                                 VDD33




                                                                                                                                  57


                                                                                                                                         56
                                                                                                                                         55
                                                                                                                                         54
                                                                                                                                         53
                                                                                                                                         52
                                                                                                                                         51
                                                                                                                                         50
                                                                                                                                         49
                                                                                                                                         48
                                                                                                                                         47
                                                                                                                                         46
                                                                                                                                         45
                                                                                                                                         44
                                                                                                                                         43
                                                          10uF          1uF         0.1uF       0.1uF                                                                                           0.1uF




                                                                                                                                                                                                                                                            15
                                                                                                                                                                                                                                                            16
                                                                                                                                                                                                                                                            17
                                                                                                                                                                                                                                                            18
                                                                                                                                                                                                                                                            19
                                                                                                                                                                                                                                                            20
                                                                                                                                                                                                                                                            21
                                                                                                                                                                                                                                                            22
                                                                                                                                                                                                                                                            23
                                                                                                                                                                                                                                                            24
                                                                                                                                                                                                                                                            25
                                                                                                                                                                                                                                                            26
                                                                                                                                               VDDA
                                                                                                                                               VDDA
                                                                                                                                   GND




                                                                                                                                              U0RXD
                                                                                                                                              U0TXD
                                                                                                                                               MTMS


                                                                                                                                               MTDO
                                                                                                                                               MTCK
                                                                                                                                             XTAL_P
                                                                                                                                             XTAL_N
                                                                                                                                             GPIO46
                                                                                                                                             GPIO45



                                                                                                                                                MTDI
                                                                                                                                         VDD3P3_CPU


                                                                                                                                             GPIO38
                                                      GND              GND      GND                GND                                                                                        GND




                                                                                                                                                                                                                                                            GPIO46

                                                                                                                                                                                                                                                            GPIO10
                                                                                                                                                                                                                                                            GPIO11
                                                                                                                                                                                                                                                            GPIO12
                                                                                                                                                                                                                                                            GPIO13
                                                                                                                                                                                                                                                            GPIO14
                                                                                                                                                                                                                                                            GPIO21
                                                                                                                                                                                                                                                            GPIO47
                                                                                                                                                                                                                                                            GPIO48
                                                                                                                                                                                                                                                            GPIO45
                                                                                                                                                                                                                                                            GPIO3

                                                                                                                                                                                                                                                            GPIO9
                                                                       50 ohm Impedance Control
                                                               1       RF_ANT        L2          TBD      LNA_IN     1                                                                   42                      GPIO37
                                                                                                                     2       LNA_IN                                             GPIO37   41                      GPIO36

反馈文档意见

                                                                                                                             VDD3P3                                             GPIO36
                                                               ANT1           C11                C12                 3
                                                                                                                             VDD3P3                                             GPIO35
                                                                                                                                                                                         40                      GPIO35                              ESP32-S3-WROOM-1U(pin-out)
                                                      2

                                                          3




                                                                                                          CHIP_PU    4                                                                   39
                                                               CONN           TBD                TBD      GPIO0      5       CHIP_PU                                            GPIO34   38
                                                                                                          GPIO1      6       GPIO0                                              GPIO33   37                      GPIO47
         40




                                                                                                          GPIO2      7       GPIO1                                            SPICLK_P   36                      GPIO48                                                  VDD_SPI
                                                      GND                       GND                GND    GPIO3      8       GPIO2                                            SPICLK_N   35   R16        0       SPID
                                                                                                          GPIO4      9       GPIO3                                                SPID   34   R15        0       SPIQ
                                                                                                                             GPIO4                                                SPIQ




                                                                                                                                                                                                                                                                           8
                                                      The values of C11, L2 and C12                       GPIO5     10
                                                                                                                             GPIO5                                              SPICLK
                                                                                                                                                                                         33   R10        0       SPICLK
                                                                                                          GPIO6     11                                                                   32                      SPICS0
                                                      vary with the actual PCB board.                                        GPIO6                                              SPICS0




                                                                                                                                                                                                                                                                            VDD
                                                                                                          GPIO7     12                                                                   31   R14        0       SPIWP                             SPICS0     1                              5      SPID
                                                                                                          GPIO8     13       GPIO7                                               SPIWP   30   R13        0       SPIHD                                             /CS                DI
                                                  B                                                                                                                                                                                                                                                                       B
                                                                                                                             GPIO8                                               SPIHD
                                                      NC: No component.                                   GPIO9     14
                                                                                                                             GPIO9                                             VDD_SPI
                                                                                                                                                                                         29                                                        SPICLK     6
                                                                                                                                                                                                                                                                   CLK               DO
                                                                                                                                                                                                                                                                                             2      SPIQ

                                                                                                                                         VDD3P3_RTC

                                                                                                                                         XTAL_32K_N
                                                                                                                                         XTAL_32K_P
                                                                                                                                                                                                                                                   SPIHD      7                              3      SPIWP
                                                                                                                                                                                                                                                                   /HOLD             /WP




                                                                                                                                                                                                                                                                            GND
                                                                                                                                                                                                C13        C14 VDD_SPI
                                                                                                                                         GPIO10
                                                                                                                                         GPIO11
                                                                                                                                         GPIO12
                                                                                                                                         GPIO13
                                                                                                                                         GPIO14



                                                                                                                                         GPIO17
                                                                                                                                         GPIO18
                                                                                                                                         GPIO19
                                                                                                                                         GPIO20
                                                                                                                                         GPIO21
                                                                                                                                         SPICS1
         ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7




                                                                                                                                                                                                0.1uF      1uF                                                     U2             FLASH




                                                                                                                                                                                                                                                                           4
                                                                                                                             U1                                           ESP32-S3
                                                                                                                                         15
                                                                                                                                         16
                                                                                                                                         17
                                                                                                                                         18
                                                                                                                                         19
                                                                                                                                         20
                                                                                                                                         21
                                                                                                                                         22
                                                                                                                                         23
                                                                                                                                         24
                                                                                                                                         25
                                                                                                                                         26
                                                                                                                                         27
                                                                                                                                         28
                                                                                                         VDD33                                                            ESP32-S3R2          GND       GND                                                                GND
                                                                                                                                                                          ESP32-S3R8
                                                                                                                                                                          ESP32-S3R16V

                                                                                                                              C15
                                                                                                                                         GPIO10
                                                                                                                                         GPIO11
                                                                                                                                         GPIO12
                                                                                                                                         GPIO13
                                                                                                                                         GPIO14

                                                                                                                                                   GPIO15
                                                                                                                                                   GPIO16
                                                                                                                                                   GPIO17
                                                                                                                                                   GPIO18
                                                                                                                                                   GPIO19
                                                                                                                                                   GPIO20
                                                                                                                                                   GPIO21




                                                                                                                             0.1uF


                                                                                                                                  GND

                                                  A                                                                                                                                                                                                                                                                       A


                                                                                                                                                 图 8-2. ESP32-S3-WROOM-1U 原理图
                                                                                                                                                                                                                              Title
                                                                                                                                                                                                                                         <ESP32-S3-WROOM-1U>

                                                                                                                                                                                                                              Size     Page Name                                   Rev
                                                                                                                                                                                                                                  A4     <02_ESP32-S3-WROOM-1U>                            Confidential and Proprietary
                                                                                                                                                                                                                                                                                    V1.5
                                                                                                                                                                                                                              Date:        Tuesday, November 21, 2023              Sheet        2        of      2
                                                                   5                                                     4                                                        3                                               2                                                         1

9 外围设计原理图

    9         外围设计原理图
    模组与外围器件（如电源、天线、复位按钮、JTAG 接口、UART 接口等）连接的应用电路图。

    VDD33                                                       GND                                          GND               VDD33
                                                                                                                                             JP1
                                                                        ESP32-S3-WROOM-1/ESP32-S3-WROOM-1U                               1
                                                                                                        41                               2    1
         C1            C3                       R1       TBD             1                        EPAD 40                                3    2
                                                                         2 GND                     GND 39       IO1                      4    3
         22uF          0.1uF                    C2       TBD    EN       3 3V3                      IO1 38      IO2                           4
                                    GND
                                                                IO4      4 EN                       IO2 37      TXD0                         UART
    GND           GND                                           IO5      5 IO4                    TXD0 36       RXD0            GND          JP2
                  C4 12pF(NC)                                   IO6      6 IO5                    RXD0 35       IO42            TMS      1
    GND                                   X1: ESR = Max. 70 K   IO7      7 IO6                     IO42 34      IO41            TDI      2    1
                                     R2




                                                                            IO7                    IO41 33                                    2
                            1




                   X1                         R3      0(NC)     IO15     8                                      IO40            TDO      3
                                              R5      0(NC)     IO16     9 IO15                    IO40 32      IO39            TCK      4    3
        32.768KHz(NC)
                                                                IO17    10 IO16                    IO39 31      IO38                          4
                                                                        11 IO17                    IO38 30
                                     NC




                                                                                                                                GND
                            2




                                                                IO18                                            IO37                         JTAG
    GND
                  C7    12pF(NC)                                IO8     12 IO18                    IO37 29      IO36                          JP4
                                                                IO19    13 IO8                     IO36 28      IO35                     2
                                                                IO20    14 IO19                    IO35 27      IO0                      1    2
    JP3                                                                     IO20                    IO0                                       1
              1        USB_D-               R6           0                                                                            Boot Option
        1


                                                                             IO46

                                                                             IO10
                                                                             IO11
                                                                             IO12
                                                                             IO13
                                                                             IO14
                                                                             IO21
                                                                             IO47
                                                                             IO48
                                                                             IO45
              2        USB_D+               R4           0
                                                                             IO3

                                                                             IO9
        2                                                                                                            SW1
    USB OTG                    C6         C5 NC: No component.                                       U1                        R7        0 EN
                                                                            15
                                                                            16
                                                                            17
                                                                            18
                                                                            19
                                                                            20
                                                                            21
                                                                            22
                                                                            23
                                                                            24
                                                                            25
                                                                            26
                            TBD           TBD                                                                   C8     0.1uF
                                                                            IO46

                                                                            IO10
                                                                            IO11
                                                                            IO12
                                                                            IO13
                                                                            IO14
                                                                            IO21
                                                                            IO47
                                                                            IO48
                                                                            IO45
                                                                            IO3

                                                                            IO9



                               GNDGND                                                                     GND

                               For ESP32-S3-WROOM-1-N16R16V and ESP32-S3-WROOM-1U-N16R16V, IO47/IO48 operates in the 1.8V voltage domain.


                                                                      图 9-1. 外围设计原理图


        • EPAD 可以不焊接到底板，但是焊接到底板的 GND 可以获得更好的散热特性。如果您想将 EPAD 焊接到底
            板，请确保使用适量焊膏，避免过量焊膏造成模组与底板距离过大，影响管脚与底板之间的贴合。

        • 为确保 ESP32-S3 芯片上电时的供电正常，EN 管脚处需要增加 RC 延迟电路。RC 通常建议为 R = 10 kΩ，
            C = 1 µF，但具体数值仍需根据模组电源的上电时序和芯片的上电复位时序进行调整。ESP32-S3 芯片的
            上电复位时序图可参考章节 4.5 芯片上电和复位。

5 4 3 2

    乐鑫信息科技                                                                    41             ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7
                                                                         反馈文档意见

10 尺寸规格

10 尺寸规格 Unit: mm

10.1 模组尺寸 18±0.2 3.1±0.15 0.8 Unit: mm 6

                                             18±0.2                                3.1±0.15
                                                                                         0.8

                                             15.8                                                                               0.9
                                                                                                                                0.5

25.5±0.2

40 x 0.9 16.51 6

                                   40 x Ø0.55




                                                                                                                                                   3.7

1.27

                                                       17.6




                                                                                                                  40 x 0.9
                                             15.8                                                                               0.9         3.7




                                                                                                                              10.29
                                         5
                                       0.




                                                                                                                                0.5




                                                                                                                              0.9
                                    Ø

25.5±0.2

                                                                         1.05
      1.5

40 x 0.9

                                   40 x Ø0.55                                                                                                       7.5

16.51

                                                                                                                                                   3.7
                          1.27




                                                       17.6




                                                                                                                   40 x 0.9
                                          13.97                                                                                            2.015
                                                                                                                                    1.27 3.7




                                                                                                                              10.29
                                        5
                                     0.




                                                                                                                              0.9
                                   40 x 0.45                                                                                        40 x 0.85
                                    Ø




                                                              1
                                                                         1.05
                 1.5




                                                                                                                                                7.5
                                           Top View                                            Side View                        Bottom View

                                          13.97                                                                                     1.27 2.015
                                   40 x 0.45                  1                                                                     40 x 0.85

                                           Top View                                            Side View                        Bottom View
                                                                                ESP32-S3-WROOM-1U Dimensions
                                                                     图 10-1. ESP32-S3-WROOM-1 模组尺寸


                                                                                ESP32-S3-WROOM-1U Dimensions
                                                                                                                                                  Unit: mm


                                             18±0.2                                3.2±0.15
                                                                     3                  0.8
                                                                                                                                                  Unit: mm

                                   10.75                                                                                        0.9
                                             18±0.2                                3.2±0.15                                     0.5
                        40 x 0.9




                                                                         2.46




                                   40 x Ø0.55                        3                  0.8
                  19.2±0.2




                                                                                                                                                   3.7




                                   15.65
                    1.27
                  16.51




                                                                                                                  40 x 0.9




                                   10.75                                                                                        0.9
                                                              13.1
                                               17.5




                                                                                                                                            3.7
                                                                                                                                    10.29
                                      5




                                                                                                                                0.5
                                                                                                                              0.9
              0.9




                                    0.
          40 x1.5




                                                                          1.1
                                                                         2.46
                                   Ø




                                   40 x Ø0.55                                                                                                       7.5
    19.2±0.2




                                                                                                                                                   3.7




                                   15.65
      1.27
    16.51




                                                                                                                   40 x 0.9




                                                                                                                                           2.015
                                                                                                                                    1.27 3.7
                                                              13.1
                                                17.5




                                          13.97
                                                                                                                                    10.29
                                       5




                                                                                                                              0.9




                                   40 x 0.45    1.08                                                                                40 x 0.85
                                    0.

1.5

                                                                         1.1
                                   Ø




                                                                                                                                                7.5
                                           Top View                                            Side View                        Bottom View

                                          13.97                                                                                     1.27 2.015
                                   40 x 0.45    1.08                 图 10-2. ESP32-S3-WROOM-1U 模组尺寸                                 40 x 0.85

                                           Top View                                            Side View                        Bottom View

说明： 有关卷带、载盘和产品标签的信息，请参阅 《ESP32-S3 模组包装信息》。

乐鑫信息科技 42 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 10 尺寸规格

10.2 外部天线连接器尺寸 ESP32-S3-WROOM-1U 采用图 10-3 外部天线连接器尺寸图 所示的第一代外部天线连接器，该连接器兼 容：

• 广濑 (Hirose) 的 U.FL 系列连接器

• I-PEX 的 MHF I 连接器

• 安费诺 (Amphenol) 的 AMC 连接器

                                                            Unit: mm




                               图 10-3. 外部天线连接器尺寸图

ESP32-S3-WROOM-1U 在认证测试过程中搭配使用的外部天线为第一代外接单极子天线，料号为

乐鑫信息科技 43 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 10 尺寸规格

TFPD05H08750011。

模组出货时不包含外部天线。请根据自身产品的使用环境与性能需求，选用适配的外部天线。

如需自行选用，建议选用满足以下要求的天线：

• 2.4 GHz 频段

• 50 Ω 阻抗

• 最大增益不超过认证中所用天线的增益 2.33 dbi

• 接口规格与模组天线连接器接口匹配，参考图 10-3 外部天线连接器尺寸图

说明： 如选用不同类型或不同增益的外部天线，除乐鑫模组已有的天线测试报告外，可能还需进行包括 EMC 在内的额外测试， 具体要求视认证类别而定。

乐鑫信息科技 44 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 11 PCB 布局建议

11 PCB 布局建议

11.1 PCB 封装图形 本章节提供以下资源供您参考：

     • 推荐 PCB 封装图，标有 PCB 设计所需的全部尺寸。详见图 11-1 ESP32-S3-WROOM-1 推荐 PCB 封装图 和
       图 11-2 ESP32-S3-WROOM-1U 推荐 PCB 封装图。

     • 推荐 PCB 封装图的源文件，用于测量图 11-1 和 11-2 中未标注的尺寸。您可用 Autodesk Viewer 查看
       ESP32-S3-WROOM-1 和 ESP32-S3-WROOM-1U 的封装图源文件。

     • ESP32-S3-WROOM-1 和 ESP32-S3-WROOM-1U 的 3D 模型。请确保下载的 3D 模型为.STEP 格式（注意，
       部分浏览器可能会加.txt 后缀）。

                                        Unit: mm
                                                   Via for thermal pad
                                                   Copper

                                                        18




                                                                                 7.49
                                                   Antenna Area
                                                                                   6
                 40 x1.5

                                         1                                40
                                          0.9
                         40 x0.9




                                          0.5
                                                                                         25.5
                16.51




                                             3.7




                                                                                 1.27
                                                            0.9




                                                     3.7
                                                                  10.29




                                             7.5
                        1.5
                        0.5




                                         15                               26

                                                   0.5    1.27
                                                   2.015 2.015
                                                       17.5


                                   图 11-1. ESP32-S3-WROOM-1 推荐 PCB 封装图

乐鑫信息科技 45 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7

                ESP32-S3-WROOM-1U Land Pattern      反馈文档意见

ESP32-S3-WROOM-1U Land Pattern 11 PCB 布局建议

                                       Unit: mm
                                                  Via for thermal pad
                                                  Copper
                                                          18
               40 x1.5

                                        1                                    40
                                         0.9




                                                                                    1.19
                       40 x0.9


                                         0.5
              16.51




                                            3.7




                                                                                       19.2
                                                                                    1.27
                                                               0.9
                                                    3.7


                                                                     10.29
                      0.5
                      1.5




                                            7.5

                                        15                                   26

                                                  0.5    1.27
                                                  2.015 2.015
                                                      17.5


                                 图 11-2. ESP32-S3-WROOM-1U 推荐 PCB 封装图

11.2 PCB 设计中的模组位置摆放 如产品采用模组进行 on-board 设计，则需注意考虑模组在底板的布局，应尽可能地减小底板对模组 PCB 天线 性能的影响。

关于 PCB 设计中模组位置摆放的更多信息，请参考 《ESP32-S3 硬件设计指南》 \> 章节 基于模组的版图设计 通用要点。

乐鑫信息科技 46 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 12 产品处理

12 产品处理

12.1 存储条件 密封在防潮袋 (MBB) 中的产品应储存在 \< 40 °C/90%RH 的非冷凝大气环境中。

模组的潮湿敏感度等级 MSL 为 3 级。

真空袋拆封后，在 25±5 °C、60%RH 下，必须在 168 小时内使用完毕，否则就需要烘烤后才能二次上线。

12.2 静电放电 (ESD) • 人体放电模式 (HBM)：±2000 V

     • 充电器件模式 (CDM)：±500 V

12.3 回流焊温度曲线 建议模组只过一次回流焊。

                                         峰值温度：235 – 250 °C
                                         峰值时间：30 – 70 s
            温度 (°C)                      焊接时间：＞ 30 s
                                         焊料：锡银铜合⾦⽆铅焊料 (SAC305)
      250

      230
      217
      200
      180


      150




      100




       50
             升温区            预热区                   焊接区                   冷却区
            25 – 150 °C   150 – 200 °C           ＞ 217 °C               ＜ 180 °C
       25    60 – 90 s     60 – 120 s            60 – 90 s             –5 ~ –1 °C/s
             1 – 3 °C/s
                                                                                      时间 (s)
        0          50        100          150      200           250

                                   图 12-1. 回流焊温度曲线

乐鑫信息科技 47 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 12 产品处理

12.4 超声波振动 请避免将乐鑫模组暴露于超声波焊接机或超声波清洗机等超声波设备的振动中。超声波设备的振动可能与模组 内部的晶振产生共振，导致晶振故障甚至失灵，进而致使模组无法工作或性能退化。

乐鑫信息科技 48 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 技术规格书版本号管理

技术规格书版本号管理

技术规格书版本 状态 水印 定义 v0.1 \~ v0.5（不 该技术规格书正在完善。对应产品处于设计阶段， 草稿 Confidential 包括 v0.5） 产品规格如有变更，恕不另行通知。 该技术规格书正在积极更新。对应产品处于验证 v0.5 \~ v1.0（不 初步 Preliminary 阶段，产品规格可能会在量产前变更，并记录在 包括 v1.0） 发布 技术规格书的修订历史中。 该技术规格书已公开发布。对应产品已量产，产 正式 v1.0 及更高版本 --- 品规格已最终确定，重大变更将通过 发布 产品变更通知 (PCN) 进行通知。 该技术规格书更新频率较低，对应产品不推荐用 任意版本 --- 不推荐用于新设计 (NRND)1 于新设计。 任意版本 --- 停产 (EOL)2 该技术规格书不再维护，对应产品已停产。 1 技术规格书涵盖的所有产品型号均不推荐用于新设计时，封面才会添加水印。 2 技术规格书涵盖的所有产品型号均停产时，封面才会添加水印。

乐鑫信息科技 49 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 相关文档和资源

相关文档和资源 相关文档 • 《ESP32-S3 技术规格书》 -- 提供 ESP32-S3 芯片的硬件技术规格。 • 《ESP32-S3 技术参考手册》 -- 提供 ESP32-S3 芯片的存储器和外设的详细使用说明。 • 《ESP32-S3 硬件设计指南》 -- 提供基于 ESP32-S3 芯片的产品设计规范。 • 《ESP32-S3 系列芯片勘误表》 -- 描述 ESP32-S3 系列芯片的已知错误。 • 证书 https://espressif.com/zh-hans/support/documents/certificates • ESP32-S3 产品/工艺变更通知 (PCN) https://espressif.com/zh-hans/support/documents/pcns?keys=ESP32-S3 • ESP32-S3 公告 -- 提供有关安全、bug、兼容性、器件可靠性的信息 https://espressif.com/zh-hans/support/documents/advisories?keys=ESP32-S3 • 文档更新和订阅通知 https://espressif.com/zh-hans/support/download/documents

开发者社区 • 《ESP32-S3 ESP-IDF 编程指南》 -- ESP-IDF 开发框架的文档中心。 • ESP-IDF 及 GitHub 上的其它开发框架 https://github.com/espressif • ESP32 论坛 -- 工程师对工程师 (E2E) 的社区，您可以在这里提出问题、解决问题、分享知识、探索观点。 https://esp32.com/ • ESP-FAQ -- 由乐鑫官方推出的针对常见问题的总结。 https://espressif.com/projects/esp-faq/zh_CN/latest/index.html • The ESP Journal -- 分享乐鑫工程师的最佳实践、技术文章和工作随笔。 https://blog.espressif.com/ • SDK 和演示、App、工具、AT 等下载资源 https://espressif.com/zh-hans/support/download/sdks-demos

产品 • ESP32-S3 系列芯片 -- ESP32-S3 全系列芯片。 https://espressif.com/zh-hans/products/socs?id=ESP32-S3 • ESP32-S3 系列模组 -- ESP32-S3 全系列模组。 https://espressif.com/zh-hans/products/modules?id=ESP32-S3 • ESP32-S3 系列开发板 -- ESP32-S3 全系列开发板。 https://espressif.com/zh-hans/products/devkits?id=ESP32-S3 • ESP Product Selector（乐鑫产品选型工具）-- 通过筛选性能参数、进行产品对比快速定位您所需要的产品。 https://products.espressif.com/#/product-selector?language=zh

联系我们 • 商务问题、技术支持、电路原理图 & PCB 设计审阅、购买样品（线上商店）、成为供应商、意见与建议 https://espressif.com/zh-hans/contact-us/sales-questions

乐鑫信息科技 50 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 修订历史

修订历史

日期 版本 发布说明 • 新增表 6-5 Active 模式下低功耗蓝牙功耗特性 2025-11-18 v1.7

                     • 新增章节 4.5 芯片上电和复位
                     • 新增章节 6.5 存储器规格
                     • 在章节 10.2 外部天线连接器尺寸 新增认证所需的外部天线信息

2025-07-25 v1.6 • 新增章节 技术规格书版本号管理 • 其他微小改动

                     • 在章节 2 功能框图 中新增关于芯片与封装内 flash/PSRAM 管脚对应关系

2025-06-10 v1.5 的注释

                     • 将模组型号 ESP32-S3-WROOM-1-N16R16V 和 ESP32-S3-WROOM-1U-
                      N16R16V 更名为 ESP32-S3-WROOM-1-N16R16VA 和 ESP32-S3-WROOM-
                      1U-N16R16VA
                     • 在章节 1.2 型号对比 的注释中新增对芯片修订信息的说明
                     • 更新章节 1.3 应用
                     • 更新章节 Strapping 管脚为章节 4 启动配置项
                     • 新增章节 5.2 外设描述

2024-11-14 v1.4 • 拆分章节 电气特性为章节 6 电气特性 和章节 7 射频特性 ，并更新格式和 措辞 • 拆分章节 模组尺寸和 PCB 封装图形为章节 10 尺寸规格 和 11 PCB 布局建 议，并新增章节 11.2 PCB 设计中的模组位置摆放 • 在章节 11.1 PCB 封装图形 中新增 ESP32-S3-WROOM-1U 的 3D 模型链接 • 更新图 12-1 回流焊温度曲线 • 其他格式和措辞的次要更新

                     • 新增模组型号 ESP32-S3-WROOM-1-N16R16VA 和 ESP32-S3-WROOM-
                      1U-N16R16VA 并更新相关信息
                     • 更新表 1-2 ESP32-S3-WROOM-1U 系列型号对比 中的表注
                     • 更新章节 4.1 芯片启动模式控制

2023-11-24 v1.3 • 更新章节 8 模组原理图 中的模组原理图 • 更新章节 10.1 模组尺寸 中的模组尺寸图 • 其他微小改动

                                                                            见下页

乐鑫信息科技 51 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 修订历史

                                      接上页

日期 版本 发布说明 • 更新章节 Strapping 管脚 • 更新章节 6.4 功耗特性 • 更新章节 7.2.1 低功耗蓝牙射频发射器 (TX) 特性 中射频发射功率的最小 值 2023-03-07 v1.2 • 更新章节 9 外围设计原理图 中的描述 • 在章节 11.1 PCB 封装图形 中增加描述 • 更新章节 12.4 • 其他微小改动

                        • 更新表 1-1 和 1-2

2022-07-22 v1.1 • 其他微小改动

                        • 更新低功耗蓝牙射频数据
                        • 更新表 6-7 内的功耗数据

2022-04-21 v1.0 • 添加认证和测试信息 • 更新章节 Strapping 管脚

2021-10-29 v0.6 全面更新，针对芯片版本 revision 1 2021-07-19 v0.5.1 预发布，针对芯片版本 revision 0

乐鑫信息科技 52 ESP32-S3-WROOM-1 & WROOM-1U 技术规格书 v1.7 反馈文档意见 免责声明和版权公告 本文档中的信息，包括供参考的 URL 地址，如有变更，恕不另行通知。 本文档可能引用了第三方的信息，所有引用的信息均为"按现状"提供，乐鑫不对信息的准确性、真实性做任何保证。 乐鑫不对本文档的内容做任何保证，包括内容的适销性、是否适用于特定用途，也不提供任何其他乐鑫提案、规格书或样 品在他处提到的任何保证。 乐鑫不对本文档是否侵犯第三方权利做任何保证，也不对使用本文档内信息导致的任何侵犯知识产权的行为负责。本文档 在此未以禁止反言或其他方式授予任何知识产权许可，不管是明示许可还是暗示许可。 Wi-Fi 联盟成员标志归 Wi-Fi 联盟所有。蓝牙标志是 Bluetooth SIG 的注册商标。 文档中提到的所有商标名称、商标和注册商标均属其各自所有者的财产，特此声明。 版权归 © 2025 乐鑫信息科技（上海）股份有限公司。保留所有权利。 www.espressif.com 

