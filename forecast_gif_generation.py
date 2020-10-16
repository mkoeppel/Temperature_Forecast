import imageio

images = []

for i in range(9):
    filename = '~/SPICED/Week_05/bokeh_screenshots/Screenshot_2020-10-16 Bokeh Application{}.png'.format(i)
    images.append(imageio.imread(filename))

imageio.mimsave('./bokeh_forecast.gif', images, fps=2)
