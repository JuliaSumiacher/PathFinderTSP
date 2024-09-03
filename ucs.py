from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {}
        # Add the node to the explored dictionary
        explored[node.state] = node.cost

        # Initialize the frontier as a Priority Queue
        frontier = PriorityQueueFrontier()
        # Add the initial node to the frontier
        frontier.add(node, node.cost)

        while not frontier.is_empty():

            # Remove a node from the frontier
            n = frontier.pop()

            # Return if the node contains a goal state
            if n.state == grid.end:
                return Solution(n, explored)

            # Generate all possible successor states
            successors = grid.get_neighbours(n.state)

            # For each successor
            for action, state in successors.items():

                # The path cost is calculated, which is the path cost of its parent plus the
                # individual cost of moving to the successor state.
                cost = n.cost + grid.get_cost(state)

                # Check if the successor is not explored or if it has been explored with a greater cost
                if state not in explored or cost < explored[state]:

                    # Initialize the son node
                    son_node = Node(value="", state=state, cost=cost, parent=n, action=action)

                    # Add the son node to the explored dictionary
                    explored[state] = cost

                    # Add the son node to the frontier
                    frontier.add(son_node, cost)

        # Fail if the frontier is empty
        return NoSolution(explored)
