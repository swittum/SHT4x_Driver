#!.venv/bin/python3
import asyncio
import datetime
import time

import matplotlib.pyplot as plt

from SHT_driver import SHT

async def main():
    # Replace with your device's UUID
    UUID_SHT = '2511E127-7CAB-66A8-915B-653A5D55A843'

    SHT_device = SHT(UUID_SHT)
    await SHT_device.connect()

    try:
        status = await SHT_device.get_battery()
        print(f'Battery status: {status}%')
        now = datetime.datetime.now()

        # Create the plot
        plt.ion()
        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex='col', figsize=(12, 12))
        for ax in (ax1, ax2, ax3):
            ax.grid()

        t = []
        temperature = []
        humidity = []
        dewpoint = []

        line1, = ax1.plot(t, temperature)
        ax1.set_ylabel('Temperature (°C)')
        ax1.set_title('Real-time Temperature Reading')

        line2, = ax2.plot(t, temperature)
        ax2.set_ylabel('Relative Humidity (%)')
        ax2.set_title('Real-time Relative Humidity Reading')

        line3, = ax3.plot(t, dewpoint)
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Dewpoint (°C)')
        ax3.set_title('Real-time Dewpoint Reading')

        time_start = time.time()

        while True:

            timestamp = time.time()-time_start
            T = await SHT_device.get_temperature()
            RH = await SHT_device.get_humidity()
            DP = await SHT_device.get_dewpoint()

            print('Time: {:.2f}'.format(timestamp))
            print('Temperature: {:.2f}'.format(T))
            print('Relative Humidity: {:.2f}'.format(RH))
            print('Dewpoint: {:.2f}\n'.format(DP))

            t.append(timestamp)
            temperature.append(T)
            humidity.append(RH)
            dewpoint.append(DP)

            line1.set_xdata(t)
            line1.set_ydata(temperature)
            ax1.relim()
            ax1.autoscale_view(True, True, True)

            line2.set_xdata(t)
            line2.set_ydata(humidity)
            ax2.relim()
            ax2.autoscale_view(True, True, True)

            line3.set_xdata(t)
            line3.set_ydata(dewpoint)
            ax3.relim()
            ax3.autoscale_view(True, True, True)

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.tight_layout()
            plt.pause(0.1)
    except:
        print('Exiting')


if __name__ == '__main__':
    asyncio.run(main())