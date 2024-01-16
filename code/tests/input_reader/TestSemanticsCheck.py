from constraint_based_simulator.input_reader import SemanticsCheck
from constraint_based_simulator.input_reader.ast.ConstantConstraint import ConstantConstraint
from constraint_based_simulator.input_reader.ast.ConstraintOperator import ConstraintOperator
from constraint_based_simulator.input_reader.ast.ConstraintType import ConstraintType
from constraint_based_simulator.input_reader.ast.Point import Point
from constraint_based_simulator.input_reader.ast.StaticQualifier import StaticQualifier


class TestSemanticsCheck:
    def testSinglePoints(self):
        assert SemanticsCheck.checkSemantics([Point(5, 4, "a")])

        assert SemanticsCheck.checkSemantics([Point(5, 4, "a"), StaticQualifier("a")])

        assert SemanticsCheck.checkSemantics([Point(5, 4, "a"), Point(20, 34, "b"), StaticQualifier("a")])

        assert not SemanticsCheck.checkSemantics([StaticQualifier("a"), Point(5, 4, "a")])

        assert not SemanticsCheck.checkSemantics([Point(5, 4, "a"), StaticQualifier("b")])

        assert not SemanticsCheck.checkSemantics([Point(5, 4, "a"), Point(5, 4, "b"), StaticQualifier("c")])

    def testConstraints(self):
        declarePoints = [Point(5, 4, "a"), Point(-30, 4, "b")]

        assert not SemanticsCheck.checkSemantics([Point(5, 4, "a"), Point(-30, 4, "a")])

        assert not SemanticsCheck.checkSemantics(
            [ConstantConstraint(ConstraintType.DISTANCE, "a", "b", ConstraintOperator.GREATER, 3)]
        )

        assert not SemanticsCheck.checkSemantics(
            [Point(5, 4, "a"), ConstantConstraint(ConstraintType.DISTANCE, "a", "a", ConstraintOperator.GREATER, 3)]
        )

        assert SemanticsCheck.checkSemantics(
            declarePoints + [ConstantConstraint(ConstraintType.DISTANCE, "a", "b", ConstraintOperator.GREATER, 3)]
        )

        assert SemanticsCheck.checkSemantics(
            declarePoints + [ConstantConstraint(ConstraintType.FORCE, "a", "b", ConstraintOperator.LESS, 3)]
        )
