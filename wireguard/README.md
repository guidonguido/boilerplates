## HowTo setup wireguard on host machine  

-  Set  `net.ipv4.ip_forward=1`
    
-  Allow connections to wireguard service: `sudo ufw allow 51820/udp`
    
-  Enable wireguard service `sudo systemctl enable wg-quick@wg0.service`
-  Create VPN service to start up WireGuard at boot
    -   `sudo systemctl start wg-quick@wg0.service` if not starting automatically ad Boot
    
    `sudo wg-quick **up**/**down** wg0` Both on Client and Server
    
    ## New Peer configuration creation
    
    ```bash
    mkdir newPeer
    cd newPeer
    wg genkey | tee private.key
    sudo chmod go= private.key
    sudo cat private.key | wg pubkey | sudo tee public.key
    sudo nano wg0.conf
    sudo wg set wg0 peer publicKey allowed-ips 192.168.10.22x
    ```
    Create QRcode of the configuration `qrencode -t ansiutf8 < wg0.conf`
    
    ### Example Config
    
    ```bash
    [Interface]
    PrivateKey = gN1lQpdingaiitMB1LoveLove/FBAdav7F/QOL634MVo=
    Address = 192.168.10.22x/24
    # PostUp = ip rule add table 200 from 192.168.1.220
    # PostUp = ip route add table 200 default via 192.168.1.254
    # PreDown = ip rule delete table 200 from 192.168.1.220
    # PreDown = ip route delete table 200 default via 192.168.1.254
    DNS = 8.8.8.8
    
    [Peer]
    PublicKey = TlzxVoVltX4jMHateHateHvSdKFFjGZe2WXwrno=
    AllowedIPs = 0.0.0.0/0                  # send all your peer’s traffic over the VPN and use the 
                                            # WireGuard Server as a gateway for all traffic
    # AllowedIPs = 192.168.10.0/24          # restrict the VPN on the peer to only connect to other peers and services on the VPN
    Endpoint = 93.51.20.186:51820
    PersistentKeepalive=30
    
    ```
