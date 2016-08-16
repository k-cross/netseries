# Packet-Switching Terms
* Wide Area Network covers a broad geographical area, larger than a city
* Local Area Network covers a limited geographical area
* Metropolitan Area Network covers a city
* OSI Model
    * Physical Layer is bits on the wire.
    * Data-Link Layer provides capability to transfer data from one device to another on a single network segment.
* Data Plane consists of the various ports that are used for the reception and transmission of packets and a forwarding table with its associated logic.
    * Responsible for packet buffering, packet scheduling, header modification, forwarding.
    * If an arriving packet's header info is found in the forwarding table, it might need header field modification and if so will be forwarded without any intervention.
* Control Plane has the main role of keeping information in the forwarding table current so that the data plane can handle as much traffic as possible.
    * Processes different control protocols that may affect the forwarding table.
    * Manage the active topology of the network
* Management Plane is used by network admins
    * Configuration and monitoring of the switch happens here
    * Extracts information or modifies data to and from the other two planes when appropriate
    * A specific protocol is used in order to communicate to this plane in a switch
## Packet Routing
* The Router Information Protocol (RIP) doesn't need to know the entire network topology in order to computer the next path
    * Works by using distance vectors
* Open Shortest Path First (OSPF) requires knowledge of the entire network topology

# Motivations for SDN
* Reduce the complexity of the control plane
* Open Source the control plane protocols
* Add functionality to the data plane and forwarding table

## Fundamental Traits of SDN
* Mostly operates on layers two and three of the OSI model
1. Plane Separation
    * Forwarding functionality deals with incoming packets based on MAC, IP, and VLAN ID characteristics.
    * Forwarding plane can forward, drop, consume or replicate packets
2. Simplified Device
    * Instead of complicated control plane software running on each device, that software is placed in the centralized controller.
    * Primitive instructions provided by control plane
3. Centralized Control
4. Network Automation and Virtualization
    * SDN can be derived from the abstractions of distributed state, forwarding, and configuration.
    * Open SDN tries to act like a sort of API for hardware and networking functions
    * Northbound and Southbound interfaces are for applications or devices respectively.
5. Openness
    * They will be well-documented, standard, and not proprietary.

## SDN Operation
* Controller
    * Contains Northbound and Southbound APIs
    * Runs on a High Performance Machine
    * Currently no standardized Northbound API
    * Allows SDN applications to define flows on the devices and to help the application respond to packets that are forwarded to the controller.
    * Keeps a global view of the network it controls, permitting optimal forwarding decisions
* SDN Devices 
    * Data drives forwarding decisions per flow (flows are unidirectional)
* Flow entries allow for simplified hardware as more calculation can happen in software
* SDN Applications are built on top of the controller and should not be confused with the OSI model
* Flows:
    * Proactive flows are defined by the application.
    * Reactive flows are responses to packets forwarded by the controller.

## SDN Devices
* Composed of an API for communcation with the controller, an abstraction layer, and a packet-processing function.

## Controllers
* Northbound API
    * Things like floodlight and opendaylight (openDaylight seems better because it uses RESTful API)
* Southbound API
    * OpenFlow (standard)
* Core Modules
    * Abstracts the details of SDN controller-to-device protocol so applications can easily communicate with devices.
    1. End-User Device Discovery: discovers devices like laptops
    2. Network Device Discovery: discovers devices that compose the network infrastructure
    3. Network Device Topology Management: Maintain information about interconnection details of devices and their direct "physical" connections
    4. Flow Management: Maintain a database of flows being managed by controller

## SDN Applications
* Applications run above the controller, interfacing with the Northbound API
* Applications gain a few things from the API
    1. Configure flows to route packets to best path end-points
    2. balance traffic loads across multiple paths
    3. react to changes in network topology
    4. redirect traffic for things like inspection, authentication, segregation, and other security related tasks
* Responsibility of app is just to perform the function for which it was designed.

## Overlay Networks and SDN
* Not an OpenSDN solution but can be thought of as a stepping stone towards one.
* They do not address the needs for flexible infrastructure, QoS, and do not drive the market to innovate network devices further.

# OpenFlow
* Defines communications protocol between the SDN data plane and control plane but does not describe the behavior of the controller itself.
* Different from legacy control plane
    1. Program different data plane elements with a common language
    2. It exists on a separate hardware device than the forwarding plane
    3. The controller can program multiple data plane elements from a single control plane instance.
* The OpenFlow controller is responsible for programming all packet-matching and forwarding rules in the switch.
