import lancedb
from RAGPipeline.store_chunks import DBConnector
import pandas as pd
pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)

db = lancedb.connect(DBConnector.DB_PATH)
table = db.open_table("vectorstore")  # or "docs" if you used default

df = table.to_arrow().to_pandas()
print(df)