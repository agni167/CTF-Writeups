#!/usr/bin/env python3

import os
from PIL import Image
import numpy as np

def calculate_edge_difference(strip1, strip2, edge_width=2):
    """
    Calculate the difference between right edge of strip1 and left edge of strip2
    Using multiple columns for better accuracy
    """
    img1 = np.array(strip1)
    img2 = np.array(strip2)
    
    right_edge = img1[:, -edge_width:, :].astype(float)
    left_edge = img2[:, :edge_width, :].astype(float)
    
    diff = np.sum((right_edge - left_edge) ** 2)
    return diff

def build_cost_matrix(strips, edge_width=2):
    """
    Build a matrix of costs for placing each strip next to each other
    """
    strip_names = list(strips.keys())
    n = len(strip_names)
    cost_matrix = np.zeros((n, n))
    
    print("Building cost matrix...")
    for i, name1 in enumerate(strip_names):
        if i % 10 == 0:
            print(f"  Processing strip {i+1}/{n}")
        for j, name2 in enumerate(strip_names):
            if i != j:
                cost_matrix[i][j] = calculate_edge_difference(strips[name1], strips[name2], edge_width)
            else:
                cost_matrix[i][j] = float('inf')
    
    return cost_matrix, strip_names

def greedy_reconstruction(cost_matrix, strip_names):
    """
    Use greedy approach: build chains by connecting best pairs
    """
    n = len(strip_names)
    
    # Find all edges and sort by cost
    edges = []
    for i in range(n):
        for j in range(n):
            if i != j:
                edges.append((cost_matrix[i][j], i, j))
    
    edges.sort()
    
    # Build chains
    right_neighbor = {}  # index -> index of right neighbor
    left_neighbor = {}   # index -> index of left neighbor
    
    for cost, i, j in edges:
        # Can only connect if i has no right neighbor and j has no left neighbor
        if i not in right_neighbor and j not in left_neighbor:
            # Check we're not creating a cycle (unless it's the final connection)
            # Trace from i backwards
            start = i
            while start in left_neighbor:
                start = left_neighbor[start]
            
            # Trace from j forwards
            end = j
            while end in right_neighbor:
                end = right_neighbor[end]
            
            # Don't connect if it creates a cycle (unless we have all strips)
            if start == end:
                continue
            
            right_neighbor[i] = j
            left_neighbor[j] = i
            
            if len(right_neighbor) == n - 1:
                break
    
    # Find the start
    start = None
    for i in range(n):
        if i not in left_neighbor:
            start = i
            break
    
    # Build order
    order = [start]
    current = start
    while current in right_neighbor:
        current = right_neighbor[current]
        order.append(current)
    
    return [strip_names[i] for i in order]

def swap_optimization(strips, order, edge_width=2, max_distance=5):
    """
    Try swapping strips to improve the reconstruction
    Look at local neighborhoods
    """
    print("\nPerforming swap optimization...")
    improved = True
    iterations = 0
    
    while improved and iterations < 10:
        improved = False
        iterations += 1
        
        for i in range(len(order) - 1):
            current_cost = 0
            if i > 0:
                current_cost += calculate_edge_difference(strips[order[i-1]], strips[order[i]], edge_width)
            current_cost += calculate_edge_difference(strips[order[i]], strips[order[i+1]], edge_width)
            if i < len(order) - 2:
                current_cost += calculate_edge_difference(strips[order[i+1]], strips[order[i+2]], edge_width)
            
            # Try swapping with nearby strips
            for j in range(max(0, i - max_distance), min(len(order), i + max_distance + 1)):
                if j == i or j == i + 1:
                    continue
                
                new_order = order[:]
                new_order[i], new_order[j] = new_order[j], new_order[i]
                
                # Calculate new cost for affected regions
                new_cost = 0
                affected = [i-1, i, i+1, j-1, j, j+1]
                for k in affected:
                    if 0 <= k < len(new_order) - 1:
                        new_cost += calculate_edge_difference(strips[new_order[k]], strips[new_order[k+1]], edge_width)
                
                old_cost = 0
                for k in affected:
                    if 0 <= k < len(order) - 1:
                        old_cost += calculate_edge_difference(strips[order[k]], strips[order[k+1]], edge_width)
                
                if new_cost < old_cost:
                    order = new_order
                    improved = True
                    print(f"  Iteration {iterations}: Swapped positions {i} and {j}")
                    break
            
            if improved:
                break
        
        if not improved:
            print(f"  Iteration {iterations}: No improvement")
    
    return order

def main():
    strips_dir = "/home/krishna/rootaccess/dancingMenNew/Dancing_Men/strips"
    
    # Load all strips
    strips = {}
    strip_files = sorted([f for f in os.listdir(strips_dir) if f.endswith('.png')])
    
    print(f"Loading {len(strip_files)} strips...")
    for filename in strip_files:
        filepath = os.path.join(strips_dir, filename)
        strips[filename] = Image.open(filepath)
    
    # Try different edge widths and pick the best
    best_order = None
    best_score = float('inf')
    
    for edge_width in [1, 2, 3]:
        print(f"\n=== Testing with edge_width={edge_width} ===")
        
        cost_matrix, strip_names = build_cost_matrix(strips, edge_width)
        order = greedy_reconstruction(cost_matrix, strip_names)
        
        # Calculate score
        score = 0
        for i in range(len(order) - 1):
            score += calculate_edge_difference(strips[order[i]], strips[order[i+1]], edge_width)
        
        print(f"Initial score: {score:.2f}")
        
        # Try to optimize
        order = swap_optimization(strips, order, edge_width, max_distance=8)
        
        # Recalculate score
        score = 0
        for i in range(len(order) - 1):
            score += calculate_edge_difference(strips[order[i]], strips[order[i+1]], edge_width)
        
        print(f"Final score: {score:.2f}")
        
        if score < best_score:
            best_score = score
            best_order = order
            print(f"*** New best! ***")
    
    print(f"\n=== Best overall score: {best_score:.2f} ===")
    
    # Create merged image
    print("\nCreating merged image...")
    first_strip = strips[best_order[0]]
    height = first_strip.height
    total_width = sum(strips[name].width for name in best_order)
    
    merged = Image.new('RGB', (total_width, height))
    x_offset = 0
    for strip_name in best_order:
        strip = strips[strip_name]
        merged.paste(strip, (x_offset, 0))
        x_offset += strip.width
    
    output_path = "/home/krishna/rootaccess/dancingMenNew/Dancing_Men/reconstructed_image.png"
    merged.save(output_path)
    
    print(f"\n✓ Saved: {output_path}")
    print(f"  Dimensions: {merged.width} x {merged.height}")
    
    # Save order
    with open("/home/krishna/rootaccess/dancingMenNew/Dancing_Men/strip_order.txt", 'w') as f:
        for i, name in enumerate(best_order, 1):
            f.write(f"{i}. {name}\n")

if __name__ == "__main__":
    main()
