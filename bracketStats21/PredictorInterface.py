
class PredictorInterface:

	def predict(self, leftName: str, rightName: str) -> (str, (float, float)):
		pass