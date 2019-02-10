echo "Setting up service..."
sudo cp robot_btn /etc/init.d/
sudo chmod +x /etc/init.d/robot_btn
sudo update-rc.d robot_btn defaults

echo "Creating logs directory..."
sudo mkdir ./logs
sudo chmod 777 ./logs

echo "Installing git..."
sudo apt-get install git

echo "Installing pip..."
sudo apt-get install python-pip
sudo apt-get install python3-pip

echo "Installing gpioero..."
sudo apt install python-gpiozero
sudo apt install python3-gpiozero

echo "Installing RPI.GPIO 0.6.3..."
sudo apt-get remove RPi.GPIO
sudo pip3 install RPi.GPIO==0.6.3

echo "Done."
