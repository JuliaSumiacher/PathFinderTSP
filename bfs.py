from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("",
                    grid.start,
                    0,
                    None,
                    None)

        # Initialize the explored dictionary to be empty
        explored = {}

        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, explored)

        # Add the node to the explored dictionary
        explored[node.state] = True

        # Initialize the frontier with the initial node
        # The frontier is a queue
        frontier = QueueFrontier()
        frontier.add(node)

        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            node = frontier.remove()

            # Generate all possible successor states
            successors = grid.get_neighbours(node.state)

            # For each successor
            for action, state in successors.items():

                # Get the successor
                new_state = state

                # Check if the successor is not explored
                if new_state not in explored:

                    # Initialize the son node
                    new_node = Node("",
                                    state,
                                    node.cost() + grid.get_cost(new_state),
                                    node,
                                    action)

                    # Mark the successor as explored
                    explored[new_state] = True

                    # Return if the node contains a goal state
                    if new_state == grid.end:
                        return Solution(new_node, explored)

                    # Add the new node to the frontier
                    frontier.add(new_node)


