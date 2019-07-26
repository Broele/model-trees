#  Copyright 2019 SCHUFA Holding AG
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class TreeNode:
    """
    A helper class to store the tree structure of a model tree.

    Do not instantiate this class directly, but used the model tree classes

    Parameters
    ----------
    depth : int, (default=0)
        Zero-based depth of the node in the tree
    estimator : object
        Base estimator of the node.
        This estimator is used in leaf nodes for predictions, but can also be stored in other nodes.
    children : list or None
        List of child nodes. Should have 2 or 0 elements or be None.
    split : Split
        Defines, how samples are split (and mapped) to the child nodes.

    Attributes
    ----------
    depth : int, (default=0)
        Zero-based depth of the node in the tree
    estimator : object
        Base estimator of the node.
        This estimator is used in leaf nodes for predictions, but can also be stored in other nodes.
    children : list or None
        List of child nodes. Should have 2 or 0 elements or be None.
    split : Split
        Defines, how samples are split (and mapped) to the child nodes.

    See Also
    --------
    modeltrees.tree.BaseModelTree : Base Model Tree implementation
    Split : Class that defines how split / mapping to the child nodes

    Notes
    -----
    This is not a sklearn estimator class, but a helper class

    """

    def __init__(self, depth=0, estimator=None, children=None, split=None):
        self.depth = depth
        self.estimator = estimator
        self.children = children
        self.split = split


class Split:
    """
    Defines a splitting of a decision / model tree node, i.e. the mapping of samples to the child node.

    This class supports splits based on one feature and threshold.
    All samples with a feature value (in the given feature) less or equal to the threshold are mapped to child 0.
    All others are mapped to child 1.

    Parameters
    ----------
    split_feature : int
        Index of the feature that is used for the split
    split_threshold : int
        Threshold for the split.

    Attributes
    ----------
    split_feature : int
        Index of the feature that is used for the split
    split_threshold : int
        Threshold for the split.
    """
    def __init__(self, split_feature, split_threshold):
        self.split_feature = split_feature
        self.split_threshold = split_threshold

    def _apply_split(self, X, y = None):
        """
        Splits a set samples according to the defines split rule in split.


        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            Input Features of the samples
        y : array-like, shape = [n_samples] or [n_samples, n_outputs], optional
            Target variable.

        Returns
        -------
        subsets: list
            A list of Subsets. If `y` is `None`, each element `i` is an array with [n_samples[i], n_features].
            Otherwise each element is a pair of input features and target variable.

        """
        # Check for left subtree
        split_filter = X[:, self.split_feature] <= self.split_threshold

        # Output depending in input
        if y is None:
            return [X[split_filter, :], X[~split_filter, :]]
        else:
            return [
                (X[split_filter, :], y[split_filter]),  # Samples for the left subtree
                (X[~split_filter, :], y[~split_filter])  # Samples for the right subtree
            ]
