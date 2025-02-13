import json
import os
import matplotlib.pyplot as plt

class MatplotlibChart:

    @staticmethod
    def generate_chart(data):
        try:
            pass
            # Exemple de génération de graphique
            # plt.plot([1, 2, 3], [4, 5, 6])
            # plt.savefig('static/total_malwares.png')

            # usb_ids = [usb['usb_id'] for usb in data['usb_analysis']]
            # total_malwares = [usb['total_malwares'] for usb in data['usb_analysis']]

            # plt.bar(usb_ids, total_malwares)
            # plt.xlabel('USB ID')
            # plt.ylabel('Total Malwares')
            # plt.title('Total Malwares per USB')

            # current_dir = os.path.dirname(os.path.abspath(__file__))
            # save_path = os.path.join(current_dir, 'static', 'total_malwares.png')
            # plt.savefig(save_path)
            # plt.close()
            # print(f"Chart saved at {save_path}")
        except Exception as e:
            print(f"Error generating chart: {e}")


