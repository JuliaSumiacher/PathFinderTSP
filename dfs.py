from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", state=grid.start, cost=0, parent=None, action=None)
        
        # Initialize the explored dictionary with the initial state
        explored = {}
        explored[node.state] = True

        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, explored)

        # Initialize the frontier with the initial node
        frontier = StackFrontier()
        frontier.add(node)

        while True:

            # Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            node = frontier.remove()

            # Get the successors
            successors = grid.get_neighbours(node.state)

            # For each successor
            for action, state in successors.items():

                # Check if the successor is not explored
                if state not in explored:

                    # Mark the successor as explored
                    explored[state] = True

                    # The path cost is calculated, which is the path cost of its parent plus the
                    # individual cost of moving to the successor state.
                    cost = node.cost + grid.get_cost(state)

                    # Initialize the son node
                    son_node = Node(value="", state=state, cost=cost, parent=node, action=action)

                    # Return if the node contains a goal state
                    if state == grid.end:
                        return Solution(son_node, explored)

                    # Add the son node to the frontier
                    frontier.add(son_node)