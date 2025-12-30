Czech Technical University in Prague

![](media/image1.png){width="1.8182655293088363in" height="1.5748031496062993in"}Faculty of Electrical Engineering

Bachelor thesis

Application of Servers and Unix-like Systems for Sensor Control in Smart Homes

Author: Weize Yuan

Supervisor: **prof. Ing. Miroslav Husák, CSc.**

Study program: Electrical Engineering and Computer Science

Prague 2025

**Official assignment**

- Printed from KOS

- For **digital version**, insert **without signatures**

- For **print**, **signed version** obtained from the **department secretary**

![](media/image2.png){width="4.876212817147857in" height="6.8831167979002625in"}

Warning: Insert all pages of multi-page assignment

**Declaration**

"I hereby declare that this bachelor's thesis is the product of my own independent work and that I have clearly stated all information sources used in the thesis according to Methodological Instruction No. 1/2009 -- "On maintaining ethical principles when working on a university final project, CTU in Prague"

Prague, date Author's signature

\...\...\...\...\...\...\..... \...\...\...\...\...\...\...\...\...\...

**Acknowledgement**

Thank here those who have helped and supported you during the research and writing process, e.g., supervisors, and family. Do not forget to thank the staff and institutions who participated in data collection or provided technical background, etc. There is a place for dedication. Exclude thesis opponent.

#  Introduction and Background

In recent years, smart home technologies have become one of the most dynamic areas in both consumer electronics and Internet of Things (IoT) research. The increasing number of connected devices and sensors in homes has led to the need for more flexible, secure, and scalable management systems.

While many commercial platforms---such as Google Home, Apple HomeKit, or Xiaomi---offer integrated smart home ecosystems, they are typically closed, cloud-dependent, and limited in terms of customization and data privacy. In contrast, Unix-like operating systems (e.g., Linux, Debian, Ubuntu) provide a powerful and open foundation for building self-hosted, transparent, and modular smart home solutions.

This thesis explores how servers running Unix-like systems can be effectively used for sensor monitoring and control within a smart home environment. Emphasis is placed on open-source frameworks such as **Home Assistant** for orchestration and **MQTT** brokers (e.g., Mosquitto, EMQX) for communication between devices.

## Background and Motivation

- Evolution of smart home technologies

- Increasing role of IoT and sensor-based automation

- Why Unix-like systems and servers are advantageous

## Problem Statement

- Limitations of typical consumer smart home systems

- Need for an open, server-based, modular architecture

## Objectives

- To analyze server applications in smart home systems

- To design and implement a model using Unix-like systems for sensor control

- To evaluate performance and compare with commercial solutions

## Methodology Overview

- Theoretical analysis → System design → Implementation → Evaluation

## Thesis Structure

### Chapter 1 -- Introduction

### Chapter 2 -- Theoretical Background(Background and Related Work)

### Chapter 3 -- System Design

### Chapter 4 -- Implementation

### Chapter 5 -- Evaluation and Results

### Chapter 6 -- Comparison and Discussion

### Chapter 7 -- Conclusion and Future Work

### Chapter 8 -- References

# Objectives

The main objective of this thesis is to design and evaluate a server-based smart home control system using Unix-like operating systems. The work will focus on three key goals:

1.  **Analytical goal:**\
    Analyze the role and advantages of servers and Unix-like systems in smart home applications, with particular focus on sensor monitoring and control.

2.  **Design goal:**\
    Design and implement a model system that uses a server to manage basic smart home functions, employing MQTT communication and Home Assistant as the control interface.

3.  **Evaluation goal:**\
    Evaluate the designed system's performance and compare it with typical commercial smart home solutions, focusing on scalability, latency, privacy, and reliability.

# System Design Overview

The proposed system follows a **multi-layer architecture**, consisting of four major layers:

  ------------------------------------------------------------------------------------------------------------------------------
  **Layer**                 **Function**                                     **Tools / Technologies**
  ------------------------- ------------------------------------------------ ---------------------------------------------------
  **Server Layer**          Hosts core services on a Unix-like environment   Debian-based VPS

  **Communication Layer**   Handles message transmission between devices     MQTT brokers (Mosquitto, EMQX)

  **Control Layer**         Provides automation logic and user interface     Home Assistant

  **Sensor Layer**          Simulates or real sensor data                    Python-based sensor simulator or physical devices
  ------------------------------------------------------------------------------------------------------------------------------

The communication between components will be achieved through **MQTT topics**, allowing asynchronous, lightweight data exchange. Multiple brokers will be deployed (Mosquitto and EMQX) to compare performance, scalability, and reliability in distributed environments.\
Home Assistant will serve as the central control and visualization interface, displaying live sensor data and allowing rule-based automation.

# Server and Service Distribution

  --------------------------------------------------------------------------------------------------------------------------
  **Server Location**   **Service(s)**          **Hardware / OS Details**
  --------------------- ----------------------- ----------------------------------------------------------------------------
  Chicago, USA          Mosquitto MQTT Broker   Debian 12.12, Kernel 6.1.0-35, Intel Xeon E5-2690 v2 1-Core,1G RAM, x86_64

  Singapore             EMQX MQTT Broker        Debian 12.11, Kernel 6.1.0-37, AMD EPYC Milan 1-Core, 3G RAM, x86_64

  Hong Kong             Sensor Simulator        Debian 12.12, Kernel 6.1.0-39, AMD EPYC 7763 2-Core, 2G RAM, x86_64

  Frankfurt, DE         Home Assistant          Debian 12.12, Kernel 6.1.0-38, ARM64 4-core CPU, 24G RAM, aarch64
  --------------------------------------------------------------------------------------------------------------------------

# Implementation Plan

The implementation will be divided into several stages:

## Stage 1 --- Environment Setup

- Deploy Docker-based services: Home Assistant, Mosquitto, EMQX deploy in different host

- Verify basic communication between components using MQTT test clients.

## Stage 2 --- Sensor Simulation(real sensor\[**ESP32,ESP8266?**\])

- Develop or adapt a Python-based MQTT sensor simulator.

- Simulate multiple sensor types (e.g., temperature, humidity) publishing to brokers

- Test MQTT connections to both Mosquitto and EMQX brokers.

## Stage 3 --- Integration with Home Assistant

- Connect Home Assistant to the brokers via MQTT integration.

- Define sensor entities and display them on the Home Assistant dashboard.

- Configure simple automation (e.g., alert if temperature exceeds threshold).

## Stage 4 --- Performance Testing

- Measure message latency, throughput, and stability under load (using emqtt-bench).

- Record and analyze results for both brokers.

- Evaluate the performance differences between distributed vs. single-server setups.

## Stage 5 --- Comparison and Evaluation

- Compare the open-source solution with commercial platforms (Google Home, Xiaomi, etc.).

- Analyze advantages in terms of openness, control, cost, and privacy.

- Summarize key findings and propose improvements.

# Expected Results

- A fully functional open-source smart home prototype based on Unix-like servers.

- Performance data and analytical comparison between Mosquitto and EMQX.

- A documented system architecture with configuration files and automation examples.

- A public GitHub repository ([SmartHome_Server](https://github.com/yuanweize/SmartHome_Server)) hosting all implementation resources.

# Tools and Technologies

- **Operating System:** Debian 12

- **Server Platform:** VPS

- **Home Automation Framework:** Home Assistant

- **MQTT Brokers:** Mosquitto, EMQX

- **Simulation Tools:** Python

- **Performance Tools:** emqtt-bench

- **Documentation:** Markdown, GitHub version control, DeepWiki

# Expected Contribution

This thesis will contribute to understanding how open-source, Unix-based server architectures can serve as a viable, efficient, and privacy-friendly alternative to proprietary smart home ecosystems. The resulting prototype will demonstrate the practicality of integrating self-hosted MQTT communication with modern automation frameworks, highlighting benefits for scalability, transparency, and customization.

![图形用户界面, 文本 AI 生成的内容可能不正确。](media/image3.png){width="8.463739063867017in" height="6.157436570428697in"}
