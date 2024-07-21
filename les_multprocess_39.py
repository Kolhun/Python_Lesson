import multiprocessing


class WarehouseManager:
    def __init__(self):
        self.data = {}

    def process_request(self, request):
        action, product, quantity = request
        if action == "receipt":
            if product in self.data:
                self.data[product] += quantity
            else:
                self.data[product] = quantity
        elif action == "shipment":
            if product in self.data and self.data[product] >= quantity:
                self.data[product] -= quantity

    def run(self, requests):
        processes = []
        for request in requests:
            process = multiprocessing.Process(target=self.process_request, args=(request,))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()


_requests = [
    ("receipt", "product1", 10),
    ("shipment", "product1", 5),
    ("receipt", "product2", 20),
    ("shipment", "product2", 15),
]

manager = WarehouseManager()
manager.run(_requests)
print(manager.data)
