# -*- coding: utf-8 -*-
"""GBIFormer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CWyeX2iGkuosFjqFSM5KgT-nqCVo67X1
"""

##===========##
##  Imports  ##
##===========##



import ast, logging, random, sys, time

#import matplotlib as mpl
import numpy      as np
import pandas     as pd
import tensorflow as tf

from matplotlib import pyplot as plt

#from google.colab import files
#uploaded = files.upload()

##====================================##
##  Config (no hard-coded variables)  ##
##====================================##

config = {
    "general" : {
        "base_seed"  : -1,
        "board_size" : 4,
    },
    "data" : {
        "input_fname"      : "combinations5.csv",    #combinationsHalfOfAll4by4s
    },
    "model" : {
        "ndim"              : 128,
        "encoder_depth"     : 4,
        "encoder_num_heads" : 8,
        "encoder_do_MLP"    : True,
        "decoder_depth"     : 4,
        "decoder_num_heads" : 8,
        "decoder_do_MLP"    : True,
        "MLP_depth"         : 3,
        "use_bias"          : True,
        "learning_rate"     : 1e-5,
    },
    "training" : {
        "epochs"           : 500,
        "batch_size"       : 32,
        "validation_split" : 0.2,
        "early_stopping" : {
            "patience" : 20,
            "monitor"  : "accuracy",
            "mode"    : "max",
        },
    },
}

##=====================##
##  Configure logging  ##
##=====================##

##  Get named logger
logger = logging.getLogger(__name__)

##  Add output handler to stdout
io_handler = logging.StreamHandler(sys.stdout)
io_handler.setFormatter(logging.Formatter("%(levelname)7s %(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
io_handler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addHandler(io_handler)

##  Test that we see output
logger.info(f"Configured for logger '{logger.name}'")

##======================================##
##  Print versions for reproducibility  ##
##======================================##

logger.info( "---------------+-----------------------------------------------------------")
logger.info( "      Package  | Version")
logger.info( "---------------+-----------------------------------------------------------")
logger.info(f"       Python  |  {sys.version}")
# logger.info(f"   Matplotlib  |  {mpl.__version__}")
logger.info(f"        Numpy  |  {np.__version__}")
logger.info(f"       Pandas  |  {pd.__version__}")
logger.info(f"   Tensorflow  |  {tf.__version__}") 

##==============##
##  Log config  ##
##==============##

def log_flattened_dictionary(logger     : logging.Logger,
                             dictionary : dict,
                             base_str   : str = "",
                             log_lvl    : int = logging.INFO,
                            ) -> None :
    """
    Recursively search through config dictionary provided and log all values found
    Dictionary keys must be castable to str
    """
    for key, val in dictionary.items() :
        if isinstance(val, dict) :
            log_flattened_dictionary(logger, val, base_str=f"{base_str} > {key}")
            continue
        logger.log(log_lvl, f"{base_str} > {key} : {val}")

logger.info("Using the following config values:")
log_flattened_dictionary(logger, config)

##==========================##
##  Configure random seeds  ##
##==========================##

##  Get base seed
base_seed = config["general"]["base_seed"]

##  If <1 then set to clock time in seconds
if base_seed < 1 :
    base_seed = int(time.time())
    logger.info(f"Setting base_seed = {base_seed}")

##  Set python seed
python_seed = base_seed
random.seed(python_seed)
logger.info(f"Python seed = {python_seed}")

##  Set numpy seed
np_seed = base_seed + 1
np.random.seed(np_seed)
logger.info(f"Numpy seed = {np_seed}")

##  Set tensorflow seed
tf_seed = base_seed + 2
tf.random.set_seed(tf_seed)
logger.info(f"Tensorflow seed = {tf_seed}")

##===========================##
##  Read input to dataframe  ##
##===========================##

##  Resolve filename
input_fname = config["data"]["input_fname"]
logger.info(f"Reading data from file {input_fname}")

##  Load file
df = pd.read_csv(
    input_fname,
)

##  Fix column heading format
df = df.T.reset_index().T.reset_index(drop=True)
df = df.set_axis(["Barrier", "Trajectory"], axis=1)

##  Log results
logger.info(f"Dataframe create with length {len(df)}:\n{str(df)}")

##=================================================##
##  Pull barriers and trajectories from dataframe  ##
##=================================================##

barriers     = list(df.iloc[:,0].map(lambda x : np.array(ast.literal_eval(x), dtype=np.int8)))
trajectories = list(df.iloc[:,1].map(lambda x : np.array(ast.literal_eval(x), dtype=np.int8)))

##==================##
##  Create X array  ##
##==================##

##  Get board size
board_size = config["general"]["board_size"]
logger.info(f"Creating data arrays according to board_size={board_size}")

##  Create list of sequences with BEGIN and END tokens
X = []
BEG, END = np.array([[board_size+1, board_size+1]]), np.array([[board_size+2, board_size+2]])
for x in trajectories :
    if len(x.shape) == 1 :
        x = x[None, :]
    x = np.concatenate([BEG, x+1, END])
    X.append(x)

##  Pad sequences with MASK token and convert to square array
max_x = max([len(x) for x in X])
X     = np.array([np.pad(x, [[0, max_x - len(x)], [0, 0]]) for x in X])

##  Log summary
logger.info(f"Data X created with shape {X.shape}")

##  Log a few datapoints
for row_idx in range(min([5, len(X)])) :
    logger.info(f"Row at index {row_idx} is:\n{X[row_idx]}")

##==================##
##  Create Y array  ##
##==================##

##  Create tensor of square arrays with 0 or 1 if there is a barrier
Y = []
for barrier in barriers :
    if len(barrier.shape) == 1 :
        barrier = barrier[None, :]
    y = np.zeros((board_size, board_size))
    for pixel in barrier :
        y[pixel[0], pixel[1]] = 1
    Y.append(y)
Y = np.array(Y)

##  Log summary
logger.info(f"Data Y created with shape {Y.shape}")

##  Log a few datapoints
for row_idx in range(min([5, len(Y)])) :
    logger.info(f"Row at index {row_idx} is:\n{Y[row_idx]}")

##===================================================================##
##  Define custom keras layer for enumerating an NxN grid of pixels  ##
##===================================================================##

# from typing import Optional

class EnumerateGrid(tf.keras.layers.Layer) :

    def __init__(self,
                 xmax : int,
                 ymax : int | None = None,
                 **kwargs
                ) :
        """
        Keras layer that outputs two flat tensors enumerating the x and y pixel locations on a grid
        Both output tensors have shape [B, xmax*ymax] where B is the batch dimension, evaluated at run-time
        by matching with a data tensor provided in the layer call
        """
        super().__init__(**kwargs)
        if ymax is None :
            ymax = xmax
        self.xmax = xmax
        self.ymax = ymax
        X, Y      = np.meshgrid(np.arange(xmax), np.arange(ymax))
        X, Y      = X.flatten(), Y.flatten()
        self.X    = tf.constant(X[None, :], dtype=self.dtype)
        self.Y    = tf.constant(Y[None, :], dtype=self.dtype)

    def call(self,
             x   : tf.Tensor,
            ) :
        """
        Create an output tensors with same batch dimension as input x
        First output tensor enumerates x positions on a grid
        Second output tensor enumerates y positions on a grid
        Both tensors have shape [B, xmax*ymax]
        """
        X = tf.tile(self.X, [tf.shape(x)[0], 1])
        Y = tf.tile(self.Y, [tf.shape(x)[0], 1])
        return X, Y

    def get_config(self) :
        """
        Create config dict, needed for saving model to file
        """
        config = super().get_config()
        config["amax"] = self.amax
        return config

##==========================================================================##
##  Define custom keras layer for slicing the right-most index of a tensor  ##
##==========================================================================##

class RightSlice(tf.keras.layers.Layer) :

    def __init__(self,
                 index       : int,
                 expand_dims : bool = False,
                 **kwargs
                ) :
        """
        Keras layer that slices a tensor along its right-most axis and returns the index provided
        """
        super().__init__(**kwargs)
        self.index       = index
        self.expand_dims = expand_dims

    def call(self,
             x   : tf.Tensor,
            ) :
        """
        Slices x along its right-most axis and returns the index provided
        Output tensor has one fewer dimensions than x unless expand_dims is set to True
        """
        ##  Slice x
        y = x[..., self.index]

        ##  Expand dims
        if self.expand_dims :
            y = y[..., None]

        ## Return
        return y

    def get_config(self) :
        """
        Create config dict, needed for saving model to file
        """
        config = super().get_config()
        config["index"      ] = self.index
        config["expand_dims"] = self.expand_dims
        return config

##====================================================##
##  Define method for creating our transformer model  ##
##====================================================##

def create_model(board_size        : int,
                 name              : str      = "Tomformer",
                 ndim              : int      = 64,
                 encoder_depth     : int      = 3,
                 encoder_num_heads : int      = 8,
                 encoder_do_MLP    : bool     = True,
                 decoder_depth     : int      = 3,
                 decoder_num_heads : int      = 8,
                 decoder_do_MLP    : bool     = True,
                 MLP_depth         : int      = 2,
                 use_bias          : bool     = True,
                 dtype                        = tf.float32,
                 dtype_in                     = tf.int8,
                 learning_rate     : float    = 1e-4,
                 loss              : str      = "binary_crossentropy",
                ) -> tf.keras.models.Model :
    """
    Create keras transformer model and compile with Adam optimiser
    """

    ##  Log model creation
    logger.info(f"Creating transformer model '{name}' with the following settings:")
    logger.info(f"          board_size: {board_size}")
    logger.info(f"                ndim: {ndim}")
    logger.info(f"       encoder_depth: {encoder_depth}")
    logger.info(f"   encoder_num_heads: {encoder_num_heads}")
    logger.info(f"      encoder_do_MLP: {encoder_do_MLP}")
    logger.info(f"       decoder_depth: {decoder_depth}")
    logger.info(f"   decoder_num_heads: {decoder_num_heads}")
    logger.info(f"      decoder_do_MLP: {decoder_do_MLP}")
    logger.info(f"           MLP_depth: {MLP_depth}")
    logger.info(f"            use_bias: {use_bias}")
    logger.info(f"               dtype: {dtype}")
    logger.info(f"            dtype_in: {dtype_in}")
    logger.info(f"        learning_rate: {learning_rate}")
    logger.info(f"                 loss: {loss}")

    ##  Input layer, size [S, 2]
    x_in = tf.keras.layers.Input(
        shape = (None, 2),
        dtype = dtype_in,
        name  = f"{name}_input",
    )

    ##  Pull x-component from input
    Vx_in = RightSlice(
        name  = f"{name}_slice_x",
        index = 0,
    )(x_in)

    ##  Embed x-component
    Vx = tf.keras.layers.Embedding(
        name       = f"{name}_encoder_embed_x",
        input_dim  = board_size + 3,
        output_dim = ndim,
        mask_zero  = True,
    )(Vx_in)

    ##  Pull y-component from input
    Vy_in = RightSlice(
        name  = f"{name}_slice_y",
        index = 0,
    )(x_in)

    ##  Embed y-component
    Vy = tf.keras.layers.Embedding(
        name       = f"{name}_encoder_embed_y",
        input_dim  = board_size + 3,
        output_dim = ndim,
        mask_zero  = True,
    )(Vy_in)

    ##  Combine x and y embeddings by addition
    x = tf.keras.layers.Add(
        name = f"{name}_encoder_combine_x_y",
    )([Vx, Vy])

    ##  Loop over encoder blocks
    for layer_idx in range(encoder_depth) :

        ##  Normalise x
        m = tf.keras.layers.LayerNormalization(
            name  = f"{name}_encoder_LN0_layer{layer_idx}",
            dtype = dtype,
        )(x)

        ##  Calculate self-attention
        m = tf.keras.layers.MultiHeadAttention(
            name      = f"{name}_encoder_MHSA_layer{layer_idx}",
            num_heads = encoder_num_heads,
            key_dim   = ndim,
            use_bias  = use_bias,
            dtype     = dtype,
        )(m, m)

        ##  Add back to residual stream
        x = tf.keras.layers.Add(
            name = f"{name}_encoder_add0_layer{layer_idx}",
        )([x, m])

        ##  If no MLP then continue loop
        if not encoder_do_MLP : continue

        ##  Normalise x
        m = tf.keras.layers.LayerNormalization(
            name  = f"{name}_encoder_LN1_layer{layer_idx}",
            dtype = dtype,
        )(x)

        ##  Calculate feed-forward block
        m = tf.keras.layers.Dense(
            name       = f"{name}_encoder_MLP0_layer{layer_idx}",
            units      = 4*ndim,
            use_bias   = use_bias,
            activation = "relu",
            dtype      = dtype,
        )(m)
        m = tf.keras.layers.Dense(
            name       = f"{name}_encoder_MLP1_layer{layer_idx}",
            units      = ndim,
            use_bias   = use_bias,
            activation = "linear",
            dtype      = dtype,
        )(m)

        ##  Add back to residual stream
        x = tf.keras.layers.Add(
            name = f"{name}_encoder_add1_layer{layer_idx}",
        )([x, m])

    ##  Normalise x
    x = tf.keras.layers.LayerNormalization(
        name  = f"{name}_encoder_post_LN",
        dtype = dtype,
    )(x)

    ##  Enumerate grid of pixels x and y for decoder
    Vx, Vy = EnumerateGrid(
        name = f"{name}_decoder_enum_grid",
        xmax = board_size,
    )(x)

    ##  Embed x-component
    Vx = tf.keras.layers.Embedding(
        name       = f"{name}_decoder_embed_x",
        input_dim  = board_size,
        output_dim = ndim,
        mask_zero  = False,
    )(Vx)

    ##  Embed y-component
    Vy = tf.keras.layers.Embedding(
        name       = f"{name}_decoder_embed_y",
        input_dim  = board_size,
        output_dim = ndim,
        mask_zero  = False,
    )(Vy)

    ##  Combine x and y embeddings by addition
    y = tf.keras.layers.Add(
        name = f"{name}_decoder_combine_x_y",
    )([Vx, Vy])

    ##  Loop over decoder blocks
    for layer_idx in range(decoder_depth) :

        ##  Normalise y
        m = tf.keras.layers.LayerNormalization(
            name  = f"{name}_decoder_LN0_layer{layer_idx}",
            dtype = dtype,
        )(y)

        ##  Calculate cross-attention
        m = tf.keras.layers.MultiHeadAttention(
            name      = f"{name}_decoder_MHCA_layer{layer_idx}",
            num_heads = decoder_num_heads,
            key_dim   = ndim,
            use_bias  = use_bias,
            dtype     = dtype,
        )(m, x)

        ##  Add back to residual stream
        y = tf.keras.layers.Add(
            name = f"{name}_decoder_add0_layer{layer_idx}",
        )([y, m])

        ##  Normalise y
        m = tf.keras.layers.LayerNormalization(
            name  = f"{name}_decoder_LN1_layer{layer_idx}",
            dtype = dtype,
        )(y)

        ##  Calculate self-attention
        m = tf.keras.layers.MultiHeadAttention(
            name      = f"{name}_decoder_MHSA_layer{layer_idx}",
            num_heads = decoder_num_heads,
            key_dim   = ndim,
            use_bias  = use_bias,
            dtype     = dtype,
        )(m, m)

        ##  Add back to residual stream
        y = tf.keras.layers.Add(
            name = f"{name}_decoder_add1_layer{layer_idx}",
        )([y, m])

        ##  If no MLP then continue loop
        if not decoder_do_MLP : continue

        ##  Normalise y
        m = tf.keras.layers.LayerNormalization(
            name  = f"{name}_decoder_LN2_layer{layer_idx}",
            dtype = dtype,
        )(y)

        ##  Calculate feed-forward block
        m = tf.keras.layers.Dense(
            name       = f"{name}_decoder_MLP0_layer{layer_idx}",
            units      = 4*ndim,
            use_bias   = use_bias,
            activation = "relu",
            dtype      = dtype,
        )(m)
        m = tf.keras.layers.Dense(
            name       = f"{name}_decoder_MLP1_layer{layer_idx}",
            units      = ndim,
            use_bias   = use_bias,
            activation = "linear",
            dtype      = dtype,
        )(m)

        ##  Add back to residual stream
        y = tf.keras.layers.Add(
            name = f"{name}_decoder_add2_layer{layer_idx}",
        )([y, m])

    ##  Loop over MLP layers
    for layer_idx in range(MLP_depth) :

        ##  Normalise y
        y = tf.keras.layers.LayerNormalization(
            name  = f"{name}_MLP_LN_layer{layer_idx}",
            dtype = dtype,
        )(y)

        ##  Calculate feed-forward block
        y = tf.keras.layers.Dense(
            name       = f"{name}_MLP_layer{layer_idx}",
            units      = 4*ndim,
            use_bias   = use_bias,
            activation = "relu",
            dtype      = dtype,
        )(y)

    y = tf.keras.layers.Dense(
        name       = f"{name}_logits",
        units      = 1,
        use_bias   = use_bias,
        activation = "sigmoid",
        dtype      = dtype,
    )(y)

    ##  Shape to map size
    y = tf.keras.layers.Reshape(
        name         = f"{name}_output",
        target_shape = (board_size, board_size),
        input_shape  = (board_size*board_size, 1),
    )(y)

    ##  Create model
    model = tf.keras.models.Model(
        x_in,
        y,
        name = name,
    )

    ##  Compile
    model.compile(
        loss      = loss,
        metrics   = ["accuracy"],
        optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=learning_rate),
    )

    ##  Log created model
    model.summary(print_fn=logger.info)

    ##  Return model
    return model

##==================================##
##  Create transformer keras model  ##
##==================================##

model = create_model(
    board_size = board_size,
    **config["model"],
)

##============================================================##
##  Shuffle and split data into training and validation sets  ##
##============================================================##

##  Enumerate datapoints and shuffle
idcs = np.arange(len(X))
np.random.shuffle(idcs)

##  Separate indices into train and validation sets
val_split            = config["training"]["validation_split"]
split_idx            = int(val_split*len(idcs))
train_idcs, val_idcs = idcs[split_idx:], idcs[:split_idx]
logger.info(f"Validation split is {val_split}")
logger.info(f"Assigned following indicies for training data: {train_idcs}")
logger.info(f"Assigned following indicies for validation data: {val_idcs}")

##  Create train and validation sets
train_X, train_Y = X[train_idcs], Y[train_idcs]
val_X  , val_Y   = X[  val_idcs], Y[  val_idcs]
logger.info(f"train_X created with shape: {train_X.shape}")
logger.info(f"train_Y created with shape: {train_Y.shape}")
logger.info(f"  val_X created with shape: {  val_X.shape}")
logger.info(f"  val_Y created with shape: {  val_Y.shape}")

##=============##
##  Fit model  ##
##=============##

##  Resolve training config
epochs     = config["training"].get("epochs", 100)
batch_size = config["training"].get("batch_size", 32)
#monitor    = config["validation_data"].get("early_stopping", {}).get("monitor" , "loss")
monitor    = config["training"].get("early_stopping", {}).get("monitor", "val_loss")
mode       = config["training"].get("early_stopping", {}).get("mode"    , "min")
patience   = config["training"].get("early_stopping", {}).get("patience", 10    )

##  Log settings
logger.info(f"Training for maximum of {epochs} epochs")
logger.info(f"Early stopping with minitor '{monitor}' and patience={patience}")

##  Fit model
model.fit(train_X,
          train_Y,
          validation_data = (val_X, val_Y),
          epochs     = epochs,
          batch_size = batch_size,
          callbacks  = [tf.keras.callbacks.EarlyStopping(monitor=monitor, patience=patience, mode=mode, restore_best_weights=True)],
         )

##================================##
##  Evaluate model on train data  ##
##================================##

evals = model.evaluate(train_X, train_Y, verbose=0)
for metric_name, metric_value in zip(model.metrics_names, evals) :
        logger.info(f"Training set: {metric_name} = {metric_value:.4}")

##=====================================##
##  Evaluate model on validation data  ##
##=====================================##

evals = model.evaluate(val_X, val_Y, verbose=0)
for metric_name, metric_value in zip(model.metrics_names, evals) :
        logger.info(f"Validation set: {metric_name} = {metric_value:.4}")



##======================================================================##
##  Define quick method for plotting a true map against its prediction  ##
##======================================================================##

def plot_maps(Y_true : np.ndarray,
              Y_pred : np.ndarray,
              X_true : np.ndarray | None = None,
              show   : bool              = True,
              close  : bool              = True,
             ) -> plt.Figure :
    """
    Plot a true pixel-map side-by-side with that predicted by a model
    Optionally also plot the true trajectory
    Returns the figure object
    """
    print(X_true)
    print(Y_true)
    ##  Create figure
    fig = plt.figure(figsize=(6.3, 3))
    fig.subplots_adjust(wspace=.3/3)

    ##  Create and format axes
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax1.tick_params(left=False, bottom=False, top=False, right=False)
    ax2.tick_params(left=False, bottom=False, top=False, right=False)
    ax1.xaxis.set_ticklabels([])
    ax2.xaxis.set_ticklabels([])
    ax1.yaxis.set_ticklabels([])
    ax2.yaxis.set_ticklabels([])
    ax1.set_title("True", weight="bold", fontsize=14)
    ax2.set_title("Pred", weight="bold", fontsize=14)

    ##  Plot pixel maps
    ax1.imshow(Y_true.T, origin="lower", cmap="Greys", vmin=0, vmax=1)
    ax2.imshow(Y_pred.T, origin="lower", cmap="Greys", vmin=0, vmax=1)

    ##  Infer number of legal squares from shape of map provided
    num_squares_x = Y_true.shape[0]
    num_squares_y = Y_true.shape[1]

    ##  Plot trajectory
    ##  N.B. we must subtract 1 from pixel locations to account for earlier offset
    if X_true is not None :
        x_last, y_last = None, None
        for x, y in X_true - 1 :
            if x < 0 or x >= num_squares_x : continue  # Ignore [MASK, BEGIN, END] tokens
            if y < 0 or y >= num_squares_y : continue  # Ignore [MASK, BEGIN, END] tokens
            ax1.plot(x, y, "o", ms=10, c="red")
            ax2.plot(x, y, "o", ms=10, c="red")
            if x_last is not None :
                ax1.plot([x_last, x], [y_last, y], "--", lw=2, c="r")
                ax2.plot([x_last, x], [y_last, y], "--", lw=2, c="r")
            x_last, y_last = x, y

    ##  Show figure
    if show :
        plt.show() # plt.show(fig)

    ##  Close figure
    if close :
        plt.close(fig)

    ##  Return figure
    return fig

##==========================================##
print("##  Plot some predictions on training data  ##")
##==========================================## 

num_print = min([3, len(train_X)])
print("train_X",train_X)
train_Y_predictions = model.predict(train_X[:num_print], verbose=0)
for row_idx in range(num_print) :
    logger.info(f"Training set row {row_idx} with")
    logger.debug(f"Y_TRUE =\n{train_Y[row_idx]}\n")
    logger.debug(f"Y_PRED =\n{train_Y_predictions[row_idx]}\n")
    plot_maps(train_Y[row_idx], train_Y_predictions[row_idx], train_X[row_idx])

##============================================##
##  Plot some predictions on validation data  ##
##============================================##

num_print = min([3, len(val_X)])
val_Y_predictions = model.predict(val_X[:num_print], verbose=0)
for row_idx in range(num_print) :
    logger.info(f"Validationn set row {row_idx} with")
    logger.debug(f"Y_TRUE =\n{val_Y[row_idx]}\n")
    logger.debug(f"Y_PRED =\n{val_Y_predictions[row_idx]}\n")
    print("val_Y_predictions[row_idx]",val_Y_predictions[row_idx])
    plot_maps(val_Y[row_idx], val_Y_predictions[row_idx], val_X[row_idx])