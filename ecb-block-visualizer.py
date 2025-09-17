#!/usr/bin/env python3
"""
AES ECB Block Visualization Tool

A tool for visualizing how data is divided into 16-byte blocks and analyzing
the effects of byte injection on block alignment for ECB mode attacks.
"""

import binascii

class ECBBlockVisualizer:
    def __init__(self, block_size=16):
        self.block_size = block_size
    
    def visualize_blocks(self, data, title="Data Blocks", show_ascii=True, show_positions=True):
        """Visualize data in blocks with clear boundaries"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        print(f"\n{title}")
        print("=" * 80)
        
        total_blocks = (len(data) + self.block_size - 1) // self.block_size
        
        for i in range(0, len(data), self.block_size):
            block = data[i:i+self.block_size]
            block_num = i // self.block_size + 1
            
            # Create visual representation
            hex_repr = binascii.hexlify(block).decode('utf-8')
            hex_formatted = ' '.join([hex_repr[j:j+2] for j in range(0, len(hex_repr), 2)])
            
            # ASCII representation
            ascii_repr = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in block])
            
            # Position markers
            positions = ' '.join([f"{i+j:2d}" for j in range(len(block))])

            print(f"Block {block_num:2d} │ {hex_formatted:<47} │ [{ascii_repr:<16}]")

            if show_positions and block_num == 1:
                print(f"Position │ {positions:<47} │")
                print("─" * 80)
            
        
        print(f"\nTotal: {len(data)} bytes, {total_blocks} blocks")
        if len(data) % self.block_size != 0:
            padding_needed = self.block_size - (len(data) % self.block_size)
            print(f"Padding needed: {padding_needed} bytes to complete last block")
    
 
    def injection_attack_demo(self, target, inject_bytes):
        """Show specific injection scenario"""
        injected_data = 'A' * inject_bytes + target
        print(f"\n🎯 INJECTION ATTACK DEMONSTRATION")
        print("=" * 60)
        print(f"Target: '{target}'")
        print(f"Injected: {inject_bytes} 'A' bytes")
        print(f"Result: '{'A' * inject_bytes}{target}'")
        
        self.visualize_blocks(target, "Original Target")
        self.visualize_blocks(injected_data, "After Injection")
        
        original_blocks = (len(target) + 15) // 16
        new_blocks = (len(injected_data) + 15) // 16
        
        if new_blocks > original_blocks:
            print(f"⚠️  Target data spread across {new_blocks - original_blocks} additional block(s)")

def main():
    print("🔐 AES ECB Block Visualization Tool")
    print("=" * 50)
    print("Block size: 16 bytes (128 bits)")
    print("This tool helps visualize ECB block boundaries and injection effects.")
    
    viz = ECBBlockVisualizer()
    
    while True:

        try:
            target = "ctf.aesflag{oQWSvPxT039eUynNH1GVecf3A8z.QX0MzN5wSO0ATNyEzW}"
            inject = int(input("Enter number of bytes to inject: "))
            viz.injection_attack_demo(target, inject)
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()